# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect

# Create your views here.
def mainLogin(request):

    if request.user.is_authenticated():
        logout(request)

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            print "LOGGED IN +++++++++++++++++++++++++++++"
            return render(request, 'login/success.html', )
        else:
            print "NOT VALID #############################"
    else:
        form = AuthenticationForm()
    return render(request, 'login/main.html', {'form': form})
    

def newuser(request):

    if request.user.is_authenticated():
        logout(request)

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            print "******************************"
            return render(request, 'login/success.html', )
    else:
        form = UserCreationForm()
    return render(request, 'login/newuser.html', {'form': form})
    #return render(request, 'login/main.html')

def success(request):
    print "Logged In &&&&&&&&&&&&&&&&&&&&&&&&&&&&"
    return render(request, 'login/success.html')

def mainLogout(request):
    logout(request)
    return render(request, 'login/main.html')

    