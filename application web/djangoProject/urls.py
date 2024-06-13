
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.LandingPage_view),
    path('home/', views.home_view),
    path('home/map', views.map_view),
    path('home/indoor/thanks/', views.thanks_view),
    path('home/indoor/bye/', views.bye_view),
    path('home/main/thanks/', views.thanks_view),
    path('home/main/bye/', views.bye_view),
    path('home/text/thanks/', views.thanks_view),
    path('home/text/bye/', views.bye_view),
    path('home/outdoor/thanks/', views.thanks_view),
    path('home/outdoor/bye/', views.bye_view),
    path('home/shop/thanks/', views.thanks_view),
    path('home/shop/bye/', views.bye_view),
    path('home/indoor/', views.indoor, name='indoor'),
    path('home/main/', views.main, name='main'),
    path('home/shop/', views.shop, name='shop'),
    path('home/text/', views.text, name='text'),
    path('home/outdoor/', views.outdoor, name='outdoor'),





]
