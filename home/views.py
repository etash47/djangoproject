# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.

def chooseApplication(request):
    if not (request.user.is_authenticated()):
        return redirect('/login/')    
    return render(request, 'home/index.html')
