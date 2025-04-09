from django.db import models
import numpy as np
from django.contrib.auth.models import User

def get_default_array():
    default_arr = np.random.rand(1536)
    return default_arr.tobytes()

class Restaurant(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=1000)
    latitud = models.CharField(max_length=250)
    longitud = models.CharField(max_length=250)
    image = models.ImageField(upload_to='nomy/images/', default='nomy/images/default.jpeg')
    emb = models.BinaryField(default=get_default_array())
    direccion = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.nombre

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return sum([review.rating for review in reviews]) / reviews.count()
        return 0

class searchahistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.query} - {self.timestamp}"

#Review y Reservation compartían campos comunes (restaurant, user, created_at). 
#Para evitar duplicación de código y mejorar la mantenibilidad del proyecto, se creó un modelo base llamado RestaurantInteraction, del cual ambos modelos heredan.
class RestaurantInteraction(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True  #No crea una tabla para esta clase

class Review(RestaurantInteraction):
    rating = models.IntegerField(default=0)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.restaurant.nombre}'

class Reservation(RestaurantInteraction):
    reservation_time = models.DateTimeField()
    number_of_people = models.IntegerField()
    special_requests = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Reserva para {self.user.username} en {self.restaurant.nombre} el {self.reservation_time}'