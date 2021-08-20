from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('city/<search_city>/', views.get_cities),
]
