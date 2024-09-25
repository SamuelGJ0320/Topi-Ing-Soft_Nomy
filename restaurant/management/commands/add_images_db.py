from django.core.management.base import BaseCommand
from restaurant.models import Restaurant
import json
import os
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import time 

# Cargar la API key de OpenAI desde el archivo .env
_ = load_dotenv('api_keys_2.env')
client = OpenAI(
    api_key=os.environ.get('openai_apikey'),
)

def fetch_image(url):
    response = requests.get(url)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))

class Command(BaseCommand):
    help = 'Add images to the database for restaurants'

    def handle(self, *args, **kwargs):
        restaurants = Restaurant.objects.all()
        max_images = 5
        requests_made = 0
        for restaurant in restaurants:
            if requests_made >= max_images:
                time.sleep(60)
                requests_made = 0

            response = client.images.generate(
                model="dall-e-2",
                prompt=f"Una escena del restaurante {restaurant.nombre}",
                size="256x256",
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url
            img = fetch_image(image_url)
            img.save(f'nomy/images/{restaurant.nombre}.jpg')           
            restaurant.image = f'nomy/images/{restaurant.nombre}.jpg'   
            restaurant.save()
            requests_made += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated restaurant images'))
