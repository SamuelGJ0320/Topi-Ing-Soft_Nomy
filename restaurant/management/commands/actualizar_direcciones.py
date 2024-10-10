from geopy.geocoders import Nominatim
from django.core.management.base import BaseCommand
from restaurant.models import Restaurant 

def obtener_direccion(lat, lon):
    geolocator = Nominatim(user_agent="restaurant_locator")
    location = geolocator.reverse((lat, lon), exactly_one=True)
    if location:
        return location.address
    return None

class Command(BaseCommand):
    help = 'Actualiza las direcciones de los restaurantes usando las coordenadas'

    def handle(self, *args, **kwargs):
        restaurantes = Restaurant.objects.all()
        
        for restaurante in restaurantes:
            if restaurante.latitud and restaurante.longitud:
                direccion = obtener_direccion(restaurante.latitud, restaurante.longitud)
                
                if direccion:
                    # Actualizar el campo 'direccion' del restaurante en la tabla del SQLite
                    restaurante.direccion = direccion
                    restaurante.save()
                    self.stdout.write(self.style.SUCCESS(f"Actualizada la dirección de {restaurante.nombre}"))
                else:
                    self.stdout.write(self.style.WARNING(f"No se pudo obtener la dirección para {restaurante.nombre}"))