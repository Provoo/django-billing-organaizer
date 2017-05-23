from django.conf.urls import include, url
from .views import PruebaApi, UserApi


urlpatterns = [
    url(r"^pruebapi/$", PruebaApi.as_view()),
    url(r"^usersjson/$", UserApi.as_view()),
    ]
