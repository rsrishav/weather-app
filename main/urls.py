from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('v2', views.index2),
    path('city/<str:search_city>/', views.get_cities),
]
