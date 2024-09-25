from django.db import models
import numpy as np

# Create your models here.
def get_default_array():
  default_arr = np.random.rand(1536)  # Adjust this to your desired default array
  return default_arr.tobytes()

class Restaurant(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=1000)
    latitud = models.CharField(max_length=250)
    longitud = models.CharField(max_length=250)
    image = models.ImageField(upload_to='nomy/images/', default='nomy/images/default.jpeg')
    emb = models.BinaryField(default=get_default_array())
    
    def __str__(self):
        return self.nombre