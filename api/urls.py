from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import TelegramUserViewSet, CityViewSet, ShopViewSet

router = DefaultRouter()

router.register(r'telegramusers', TelegramUserViewSet, basename='telegramusers')
router.register(r'cities', CityViewSet, basename='cities')
router.register(r'shops', ShopViewSet, basename='shops')

urlpatterns = [
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken')),
]
