# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


def default(request):
    return render(request, 'vnaControl/vna_control.html')

# Create your views here.
