from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^location/(?P<id>\d+)/$', views.weather_query, name = "weather"),
]
