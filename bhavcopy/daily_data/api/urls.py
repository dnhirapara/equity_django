from django.contrib import admin
from django.urls import path, include
from .views import get_list, get_demo, get_csv

urlpatterns = [
    path('', get_list, name="data"),
    path('demo', get_demo, name='demo'),
    path('getcsv/<str:key>/', get_csv, name='getcsv')
]
