from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users.views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from apps.app.views import (FormatViewset,ProTypeViewset,AllProTypeViewset,StorageViewset,ProductViewset,ClientViewset,OutcomeViewset,IncomeViewset,PaymentsViewset, ServiceTypeViewset,Addition_serviceViewset)
router = DefaultRouter()
router.register("directors", DirectorViewset, basename="director")
router.register("managers", ManagerViewset, basename="manager")
router.register("users", UserViewset, basename="user")

router = DefaultRouter()
router.register("formats", FormatViewset, basename="formats")
router.register("protypes", ProTypeViewset, basename="protype")
router.register("all-protypes", AllProTypeViewset, basename="all-protypes")
router.register("storages", StorageViewset, basename="storages")
router.register("products", ProductViewset, basename="product")
router.register("clients", ClientViewset, basename="client")
router.register("outcomes", OutcomeViewset, basename="outcome")
router.register("incomes", IncomeViewset, basename="income")
router.register("payments", PaymentsViewset, basename="payments")
router.register("service-types", ServiceTypeViewset, basename="service-type")
router.register("addition-services", Addition_serviceViewset, basename="addition-service")


urlpatterns = [
    path("", include(router.urls)),
    path("auth-token", obtain_auth_token, name="api_token_auth"),
    path("users/me", UserMeView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
