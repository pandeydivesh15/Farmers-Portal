from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index_page, name="welcome"),
    # url(r'^search/$', views.query_result, name="search"),
    # url(r'^aboutus/$', views.about_us, name="aboutus"),
]
