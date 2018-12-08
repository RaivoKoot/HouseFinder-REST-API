from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('addresses', views.AddressView)
router.register('images', views.ImageView)
router.register('propertys',views.PropertyView, basename="propertys")

urlpatterns = [
    path('', include(router.urls)),
]
