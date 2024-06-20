from django.db import models

from django_rest_aiogram_shop.models import BaseTimeStampedModel


class TelegramUser(BaseTimeStampedModel):
    id = models.BigIntegerField(primary_key=True, db_index=True)
    related_shop = models.ForeignKey('Shop', on_delete=models.CASCADE, related_name='users', verbose_name='Shop',
                                     blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.related_shop}"


class ActiveProductManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Product(BaseTimeStampedModel):
    name = models.CharField(max_length=64, verbose_name='Name')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products', verbose_name='Category', db_index=True)
    is_active = models.BooleanField(default=True, verbose_name='Is active', db_index=True)
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True, verbose_name='Image')
    active_objects = ActiveProductManager()
    objects = models.Manager()

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class Category(BaseTimeStampedModel):
    name = models.CharField(max_length=64, verbose_name='Category name')

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Cart(BaseTimeStampedModel):
    user = models.ForeignKey('TelegramUser', on_delete=models.CASCADE, verbose_name='User')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Product')
    quantity = models.PositiveIntegerField(null=False, default=1, verbose_name='Quantity')

    class Meta:
        db_table = 'cart'
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        constraints = [
            models.UniqueConstraint(fields=['product', 'user'], name='unique_cart_item')
        ]

    def __str__(self):
        return f'{self.user} - {self.product} - {self.quantity}'


class Amount(BaseTimeStampedModel):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Product')
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, verbose_name='Shop', db_index=True)
    quantity = models.PositiveIntegerField(verbose_name='Quantity', null=True)

    class Meta:
        db_table = 'amounts'
        verbose_name = 'Amount'
        verbose_name_plural = 'Amounts'
        constraints = [
            models.UniqueConstraint(fields=['product', 'shop'], name='unique_product_shop')
        ]

    def __str__(self):
        return f'{self.shop.address} - {self.quantity}'


class Shop(BaseTimeStampedModel):
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='City', related_name='shops', db_index=True)
    address = models.CharField(max_length=64, verbose_name='Address')

    class Meta:
        db_table = 'shops'
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'

    def __str__(self):
        return f'{self.city.name} - {self.address}'


class City(BaseTimeStampedModel):
    name = models.CharField(max_length=64, verbose_name='City name')

    class Meta:
        db_table = 'cities'
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name
