from rest_framework.serializers import ModelSerializer, StringRelatedField, ValidationError, PrimaryKeyRelatedField

from shop.models import TelegramUser, Product, Category, Shop, City, Cart


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = fields


class ShopSerializer(ModelSerializer):
    city = StringRelatedField(read_only=True)

    class Meta:
        model = Shop
        fields = ('id', 'address', 'city')
        read_only_fields = fields


class ShopSerializerWithoutCity(ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'address')
        read_only_fields = fields


class CitySerializer(ModelSerializer):

    class Meta:
        model = City
        fields = ('id', 'name')
        read_only_fields = fields


class TelegramUserSerializer(ModelSerializer):
    related_shop = PrimaryKeyRelatedField(queryset=Shop.objects.only('id').all())

    class Meta:
        model = TelegramUser
        fields = ('id', 'related_shop', 'created_at')
        read_only_fields = ('created_at', )

    def validate_id(self, value):
        if not isinstance(value, int):
            raise ValidationError("id must be integer")
        return value


class ProductSerializerWithoutCategory(ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'image', 'is_active')
        read_only_fields = fields


class CartSerializer(ModelSerializer):
    product = ProductSerializerWithoutCategory(read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'product', 'quantity', 'updated_at')
        read_only_fields = fields


class ProductSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'description', 'price', 'image', 'is_active')
        read_only_fields = fields
