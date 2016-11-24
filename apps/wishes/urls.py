from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^add$', views.add),
    url(r'^add_wish$', views.add_wish),
    url(r'^wish_items/(?P<id>\d+)$', views.wish_items),
    url(r'^join/(?P<id>\d+)$', views.join, name='join'),
    url(r'^delete/(?P<wish_id>\d+)$', views.delete),
    url(r'^remove/(?P<wish_id>\d+)$', views.remove),
    url(r'^logout$', views.logout),
]
