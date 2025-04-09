from django.urls import path
from views import ReservationCreateView, restaurant, add_review, account_view

urlpatterns = [
    path('', restaurant, name='restaurant'),
    path('restaurant/<int:restaurant_id>/review/', add_review, name='add_review'),  # Ruta para añadir reseñas
    path('account/', account_view, name='account'), # Ruta para la vista de la cuenta
    path('reservation/', ReservationCreateView.as_view(), name='reservation'), # Ruta para la vista de la reserva
]