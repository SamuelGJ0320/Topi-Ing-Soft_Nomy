from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Restaurant, searchahistory, Review, Reservation
from .recommender_provider import RecommenderProvider  # Nuevo import
import openai
import os
from dotenv import load_dotenv
from twilio.rest import Client
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import ReservationForm


# Cargar las claves de API
load_dotenv('api_keys_1.env')
load_dotenv('api_keys_2.env')
api_key = os.getenv('openai_apikey')
openai.api_key = api_key

def home(request):
    return render(request, 'home.html')

def restaurant(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')

        if request.user.is_authenticated:
            searchahistory.objects.create(user=request.user, query=prompt)

        recommender = RecommenderProvider.get_instance()
        restaurants, best_restaurant = recommender.get_recommendations(prompt)

    else:
        best_restaurant = []
        restaurants = Restaurant.objects.all()

    return render(request, 'restaurant.html', {
        'restaurants': restaurants,
        'recommendations': best_restaurant
    })

@login_required(login_url='/login/')
def add_review(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        rating = int(request.POST.get('rating', 0))
        comment = request.POST.get('comment', '').strip()

        if 1 <= rating <= 5:
            Review.objects.create(
                restaurant=restaurant,
                user=request.user,
                rating=rating,
                comment=comment
            )
            messages.success(request, "Gracias por tu reseña!")
        else:
            messages.error(request, "Selecciona una calificación válida.")

        return redirect('restaurant')

    rating_range = range(1, 6)
    return render(request, 'submit_review.html', {
        'restaurant': restaurant,
        'rating_range': rating_range
    })

@login_required(login_url='/login/')
def account_view(request):
    search_history = searchahistory.objects.filter(user=request.user).order_by('-timestamp')
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'account.html', {'search_history': search_history, 'reviews': reviews})
class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservar.html'
    success_url = reverse_lazy('restaurant')
    login_url = '/login/' 

    def form_valid(self, form):
        form.instance.user = self.request.user  # Asocia reserva al usuario
        response = super().form_valid(form)
        whatsapp_notification(self.object)  # Notificación por WhatsApp
        messages.success(self.request, f'Reserva realizada exitosamente en {self.object.restaurant.nombre}')
        return response
    
def whatsapp_notification(reservation):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    twilio_number = os.getenv('TWILIO_PHONE_NUMBER')
    default_whatsapp_number = os.getenv('DEFAULT_WHATSAPP')

    client = Client(account_sid, auth_token)

    message = f"Reserva realizada en {reservation.restaurant.nombre} para {reservation.number_of_people} personas el {reservation.reservation_time}."
    try:
        client.messages.create(
            body=message,
            from_=twilio_number,
            to=default_whatsapp_number
        )
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")
        return False
    return True