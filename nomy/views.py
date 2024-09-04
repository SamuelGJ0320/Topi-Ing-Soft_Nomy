from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Nomy
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    searchTerm = request.GET.get('searchNomy')
    if searchTerm:
        nomys = Nomy.objects.filter(title__icontains=searchTerm)
    else:
        nomys = Nomy.objects.all()
    return render(request,'home.html', {'searchTerm':searchTerm, 'nomys': nomys})

def about(request):
    return render(request,'about.html')

def map(request):
    return render(request,'map.html')

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('http://127.0.0.1:8000/')
        
        else:
            messages.info(request,'Username OR password is incorrect')
        
    return render(request,'login.html')

def logoutUser(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/login/')

def register(request):
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