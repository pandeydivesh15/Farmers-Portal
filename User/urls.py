from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^login/$', views.check_login, name="login"),
    url(r'^signup/$', views.signup_user, name="signup"),
    url(r'^logout/$', views.logout_user, name="logout"),
    url(r'^profile/$', views.view_profile, name="profile"),
]
