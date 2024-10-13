from django.urls import path
from . import views

urlpatterns = [
    path('', views.restaurant, name='restaurant'),
    path('restaurant/<int:restaurant_id>/review/', views.add_review, name='add_review'),  # Ruta para añadir reseñas
]
