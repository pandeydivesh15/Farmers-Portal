from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index_page, name="welcome"),
    url(r'^query/(?P<id>\d+)/$', views.query_resolve, name="query"),
    url(r'^query/search/(?P<id>\d+)/$', views.search_database, name="search"),
    url(r'^faq/$', views.get_faq, name="faq"),
    url(r'^aboutus/$', views.about_us, name="aboutus"),
]
