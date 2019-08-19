from django.conf.urls import url, include
from rest_framework import routers
from server_api import views


router = routers.DefaultRouter()
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('server_api.urls')),
    url(r'^', views.index),
]