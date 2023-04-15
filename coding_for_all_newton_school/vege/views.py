from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, login
from django.contrib.auth.decorators import login_required

@login_required(login_url='/user_login/')
def recipe(request):
    if request.method == 'POST':
        data = request.POST
        name = data.get('receipe_name')
        description = data.get('receipe_description')
        image = request.FILES.get('receipe_image')
        
        Recipe.objects.create(
            receipe_name=name,
            receipe_description=description,
            receipe_image=image,
            user = request.user # add user id to the relevant receipe
            )
        return redirect('/receipe')
    
    # Query all recipes from the database for the logged in User only.
    #queryset = Recipe.objects.all()
    queryset = Recipe.objects.filter(user=request.user)
    context = {
        'receipes' : queryset
    }    
    return render(request, 'receipe.html',context)

@login_required(login_url='/user_login/')
def delete_receipe(request,id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    return redirect('/receipe')

@login_required(login_url='/user_login/')
def update_receipe(request,id):
    queryset = Recipe.objects.get(id=id)
    if request.method == 'POST':
        data = request.POST
        queryset.receipe_name = data.get('receipe_name')
        queryset.receipe_description = data.get('receipe_description')
        image = request.FILES.get('receipe_image')
        if image:
            queryset.receipe_image = request.FILES.get('receipe_image')
            
        queryset.save()
        return redirect('/receipe')
    context = {
        'receipe' : queryset
    } 
    return render(request, 'update_receipe.html',context)

def user_login(request):
    if request.method == 'POST':
        data = request.POST
        email = data.get('email')
        password = data.get('password')
        
        # Check Username already exists or not
        if not User.objects.filter(username=email).exists():
            messages.error(request, f'{email} UserName Does not Exists.')
            return redirect('/user_login/')
        user = authenticate(request, username=email, password=password)
        
        if user is None:
            messages.error(request, 'Invalid UserName / Password.')
            return redirect('/user_login/')
        else:
            login(request,user)
            return redirect('/receipe/')
        
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/user_login/')

def register(request):
    if request.method == 'POST':
        data = request.POST
        fname = data.get('fname')
        lname = data.get('lname')
        email = data.get('email')
        password = data.get('password')
        
        # Check Username already exists or not
        user = User.objects.filter(username=email)
        if user.exists():
            messages.info(request, f'{email} already exists.')
            return redirect('/register/')
        
        user = User.objects.create(
            first_name=fname,
            last_name=lname,
            username=email,
            email=email
            )
        user.set_password(password)
        user.save()
        messages.success(request, f'{email} Created Succesfully.')
        return redirect('/register/')
    return render(request, 'register.html')