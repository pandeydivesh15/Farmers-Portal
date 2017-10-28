from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    #url(r'^$', views.posts_list, name = "list"),
    url(r'^(?P<id>\d+)/$', views.posts_detail, name = "detail"),
    url(r'^create$', views.posts_create, name = "create"),
    url(r'^(?P<id>\d+)/edit/$', views.posts_update, name = "update"),
    url(r'^(?P<id>\d+)/delete$', views.posts_delete, name = "delete"),
]

