from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.landing, name="landing"),
    url(r'resulting-vapor', views.result, name="result"),
]
