
from django.shortcuts import render

from .models import Restaurant
import openai
from .models import Restaurant, searchahistory


from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant, searchahistory, Review

import openai
import numpy as np
import os
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


load_dotenv('api_keys_1.env')
# Cargar las variables de entorno desde el archivo .env
load_dotenv('api_keys_2.env')
api_key = os.getenv('openai_apikey')
openai.api_key = api_key

def home(request):
    return render(request, 'home.html')

# Crear tu función para obtener el embedding
def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    response = openai.Embedding.create(input=[text], model=model)
    return response['data'][0]['embedding']

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def restaurant(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')

        if request.user.is_authenticated:
            searchahistory.objects.create(user=request.user, query=prompt)

        restaurants = Restaurant.objects.all()

        emb_request = get_embedding(prompt)

        sim = []
        for i in range(len(restaurants)):
            emb = restaurants[i].emb
            emb = list(np.frombuffer(emb))
            sim.append(cosine_similarity(emb, emb_request))
        sim = np.array(sim)
        idx = np.argmax(sim)
        idx = int(idx)

        if sim[idx] > 0:
            best_restaurant = [restaurants[idx]]
        else:
            best_restaurant = []
    else:
        best_restaurant = []
        restaurants = Restaurant.objects.all()

    return render(request, 'restaurant.html', {'restaurants': restaurants, 'recommendations': best_restaurant})

def add_review(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(restaurant=restaurant, user=request.user, rating=rating, comment=comment)
        return redirect('restaurant')

    rating_range = range(1, 6)  # Esto es lo que enviamos al template
    return render(request, 'submit_review.html', {'restaurant': restaurant, 'rating_range': rating_range})
