from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from users_service.users.api.views import UserViewSet
from users_service.addresses.api.views import AddressViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("addresses", AddressViewSet)


app_name = "api"
urlpatterns = router.urls
