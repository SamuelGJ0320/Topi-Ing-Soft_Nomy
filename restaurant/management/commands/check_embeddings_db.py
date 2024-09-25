from django.core.management.base import BaseCommand
from restaurant.models import Restaurant
import json
import os
import numpy as np

class Command(BaseCommand):
    help = 'Modify path of images'

    def handle(self, *args, **kwargs):
  
        items = Restaurant.objects.all()
        item = items[10]
        print(item.emb)
        
        