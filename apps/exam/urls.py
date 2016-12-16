from django.conf.urls import url
from . import views
# from django.contrib import admin

urlpatterns = [
    url(r'^dashboard/$', views.dashboard, name = 'dashboard'),
    url(r'^item/(?P<id>\d+)$', views.item, name = 'item'),
    url(r'^item/create_form$', views.new_item, name = 'new_item'),
    url(r'^item/create$', views.create, name = 'create'),
    url(r'^logout/$', views.logout, name = 'logout'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name = 'delete'),
    url(r'^remove/(?P<id>\d+)$', views.remove, name = 'remove'),
    url(r'^add/(?P<id>\d+)$', views.add, name = 'add'),
]
