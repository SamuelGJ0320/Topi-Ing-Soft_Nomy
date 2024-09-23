from django.shortcuts import render
from .models import Restaurant

# Create your views here.
def restaurant(request):
    search_term = request.GET.get('searchRestaurant', '')
    
    if search_term:
        restaurants = Restaurant.objects.filter(nombre__icontains=search_term)
    else:
        restaurants = Restaurant.objects.all()
    
    
    return render(request, 'restaurant.html', {'restaurants': restaurants})