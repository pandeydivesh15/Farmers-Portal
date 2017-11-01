from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^register$', views.register_crop, name="register"),
    url(r'^view/$', views.view_crops, name="detail"),
    url(r'^delete/(?P<id>\d+)/$', views.crop_delete, name="delete"),
	url(r'^tag_disease/(?P<id>\d+)/$', views.tag_disease, name="disease"),
	url(r'^tag_disease/(?P<id>\d+)/crop/(?P<crop_id>\d+)$', views.tag_disease, name="disease"),
]
