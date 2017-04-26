from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^quotes$', views.quotes),
    url(r'^submitquote$', views.submitquote),
    url(r'^favorite/(?P<id>\d+)$', views.addfavorite),
    url(r'^unfavorite/(?P<id>\d+)$', views.removefavorite),
    url(r'^users/(?P<id>\d+)$', views.users)


]
