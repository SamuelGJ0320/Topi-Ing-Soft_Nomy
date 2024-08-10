from django.shortcuts import render
from django.http import HttpResponse

from .models import Nomy

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html')
    #return render(request,'home.html', {'name':'Samuel Gutierrez'})
    searchTerm = request.GET.get('searchNomy')
    if searchTerm:
        nomys = Nomy.objects.filter(title__icontains=searchTerm)
    else:
        nomys = Nomy.objects.all()
    return render(request,'home.html', {'searchTerm':searchTerm, 'nomys': nomys})

def about(request):
    #return HttpResponse('<h1>Welcome to About Page</h1>')
    return render(request,'about.html')