from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from .models import Nomy
from .forms import NomyForm, CreateUserForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

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

def loginPage(request):
    #return HttpResponse('<h1>Welcome to Login Page</h1>')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('http://127.0.0.1:8000/')
        
        else:
            messages.info(request,'Username or Password is incorrect')
        
    context = {}
    return render(request,'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/login/')

def register(request):
    #return HttpResponse('<h1>Welcome to Register Page</h1>')
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Account was created for ' + user)

            return redirect('http://127.0.0.1:8000/login/')



    context = {'form': form}
    return render(request,'register.html', context)