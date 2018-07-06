# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import Preference 
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Create your views here.

def options(request):
    
    print("Tryna customize!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    if not (request.user.is_authenticated()):
        return redirect('/login/')

    theUsername = request.user.username

    if (request.GET.get('option1')):
        Preference.objects.filter(username=theUsername).delete()
        Preference.objects.create(username=theUsername, customOption=1)
        return redirect('/home/')

    elif (request.GET.get('option2')):
        Preference.objects.filter(username=theUsername).delete()
        Preference.objects.create(username=theUsername, customOption=2)
        return redirect('/home/')
        
    elif (request.GET.get('option3')):
        Preference.objects.filter(username=theUsername).delete()
        Preference.objects.create(username=theUsername, customOption=3)
        return redirect('/home/')

    elif (request.GET.get('option4')):
        Preference.objects.filter(username=theUsername).delete()
        Preference.objects.create(username=theUsername, customOption=4)
        return redirect('/home/')

    return render(request, 'customize/options.html')