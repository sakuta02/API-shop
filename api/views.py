from django.db.utils import IntegrityError
from rest_framework import status, decorators
from rest_framework.response import Response

from api.mixins import ReturnModelViewSetMixin, ReturnReadOnlyModelViewSetMixin
from api.serializers import TelegramUserSerializer, ProductSerializer, CitySerializer, ShopSerializer, \
    ShopSerializerWithoutCity, CategorySerializer, ProductSerializerWithoutCategory, CartSerializer
from shop.models import TelegramUser, Shop, Amount, City, Cart, Category


class TelegramUserViewSet(ReturnModelViewSetMixin):
    value = 'user'
    plural_value = 'users'
    queryset = TelegramUser.objects.select_related('related_shop', 'related_shop__city').all()
    cart_queryset = Cart.objects.select_related('product', 'product__category').only('product', 'quantity')
    serializer_class = TelegramUserSerializer

    @decorators.action(methods=['get'], detail=True)
    def city(self, request, pk=None):
        city = self.get_object().related_shop.city
        data = CitySerializer(city).data
        return Response({"city": data})

    @decorators.action(methods=['get'], detail=True)
    def shop(self, request, pk=None):
        shop = self.get_object().related_shop
        if shop:
            data = ShopSerializer(shop).data
        else:
            data = None
        return Response({"shop": data})

    @decorators.action(detail=True, methods=['post', 'delete', 'put'], url_path='cart/(?P<product_pk>[^/.]+)')
    def manipulate_cart(self, request, pk=None, product_pk=None):
        if request.method == "POST":
            try:
                quantity = request.data.get('quantity', 1)
                Cart.objects.create(product_id=product_pk, user_id=pk, quantity=quantity)
            except IntegrityError:
                return Response(
                    {"detail": "Product is already in the cart or the user doesn't exist"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif request.method == "PUT":
            try:
                obj = Cart.objects.get(product_id=product_pk, user_id=pk)
                obj.quantity = request.data.get('quantity', 1)
                obj.save()
            except Cart.DoesNotExist:
                return Response(
                    {"detail": "Product is not in the cart or the user doesn't exist"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif request.method == "DELETE":
            try:
                Cart.objects.get(product_id=product_pk, user_id=pk).delete()
            except Cart.DoesNotExist:
                return Response(
                    {"detail": "Product is not in the cart or the user doesn't exist"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response({"message": "success"})

    @decorators.action(methods=['get'], detail=True, url_path='cart')
    def show_cart(self, request, pk=None):
        cart = self.cart_queryset.filter(user_id=pk)
        if cart:
            data = CartSerializer(cart, many=True).data
            return Response({'cart': data})
        else:
            return Response({'detail': 'No products in cart found'}, status=status.HTTP_400_BAD_REQUEST)


class CityViewSet(ReturnReadOnlyModelViewSetMixin):
    value = 'city'
    plural_value = 'cities'
    queryset = City.objects
    serializer_class = CitySerializer

    @decorators.action(methods=['get'], detail=True, url_path='shops')
    def shops(self, request, pk=None):
        try:
            obj = self.queryset.prefetch_related('shops').get(id=pk)
            data = {
                'id': obj.id,
                'name': obj.name,
                'shops': ShopSerializerWithoutCity(obj.shops, many=True).data
            }
            return Response(data)
        except City.DoesNotExist:
            return Response({'detail': "No City matches the given query."}, status=status.HTTP_404_NOT_FOUND)


class ShopViewSet(ReturnReadOnlyModelViewSetMixin):
    value = 'shop'
    plural_value = 'shops'
    queryset = Shop.objects.select_related('city')
    serializer_class = ShopSerializer
    queryset_amount_product = Amount.objects.select_related('product', 'product__category').only('product')
    queryset_amount_category = Amount.objects.select_related('product__category').only('product__category')
    queryset_amount_product_category = (
        Amount.objects.select_related('product', 'product__category')
        .only('product__id',
              'product__name',
              'product__category',
              'product__description',
              'product__price',
              'product__image',
              'product__is_active',
              'product__category__id'
              )
    )

    @decorators.action(methods=['get'], detail=True)
    def products(self, request, pk=None):
        products = list(map(lambda obj: obj.product, self.queryset_amount_product.filter(shop_id=pk)))
        if products:
            data = ProductSerializer(products, many=True).data
            return Response({'products': data})
        else:
            return Response({"detail": "No products are sold in this shop."}, status=status.HTTP_404_NOT_FOUND)

    @decorators.action(methods=['get'], detail=True, url_path='products/(?P<product_pk>[^/.]+)')
    def product_detail(self, request, pk=None, product_pk=None):
        try:
            amount_object = self.queryset_amount_product.get(shop_id=pk, product__pk=product_pk)
            data = ProductSerializer(amount_object.product).data
            return Response({'product': data})
        except Amount.DoesNotExist:
            return Response({"detail": "This product is not sold in this shop."}, status=status.HTTP_404_NOT_FOUND)

    @decorators.action(methods=['get'], detail=True, url_path='categories')
    def categories(self, request, pk=None):
        categories = list(map(lambda obj: obj.product.category, self.queryset_amount_category.filter(shop_id=pk)))
        if categories:
            data = CategorySerializer(categories, many=True).data
            return Response({'categories': data})
        else:
            return Response({"detail": "No products are sold in this shop."}, status=status.HTTP_404_NOT_FOUND)

    @decorators.action(methods=['get'], detail=True, url_path='categories/(?P<category_pk>[^/.]+)')
    def category_detail(self, request, pk=None, category_pk=None):
        category = Category.objects.get(id=category_pk)
        products = list(
            map(lambda obj: obj.product, self.queryset_amount_product_category.filter(product__category=category)))
        if products:
            data = {
                'id': category.id,
                'name': category.name,
                'products': ProductSerializerWithoutCategory(products, many=True).data}
            return Response(data)
        else:
            return Response({"detail": "No products are sold in this shop."}, status=status.HTTP_404_NOT_FOUND)
