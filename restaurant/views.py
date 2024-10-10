from django.shortcuts import render
from .models import Restaurant, searchahistory
from openai import OpenAI
import openai
import numpy as np
import os
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

load_dotenv('api_keys_2.env')
api_key = os.getenv('openai_apikey')
openai.api_key = api_key

def home(request):
    return render(request, 'home.html')

# Create your views here.
def get_embedding(text, client, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def restaurant(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')

        if request.user.is_authenticated:
            searchahistory.objects.create(user=request.user, query=prompt)

        restaurants = Restaurant.objects.all()

        emb_request = get_embedding(prompt, openai)

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