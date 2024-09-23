from django.db import models

# Create your models here.
class Restaurant(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=250)
    latitud = models.CharField(max_length=250)
    longitud = models.CharField(max_length=250)
    image = models.ImageField(upload_to='media/nomy/images/', default='media/nomy/images/default.jpeg')
    
    def __str__(self):
        return self.nombre