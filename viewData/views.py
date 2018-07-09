# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from fitting.models import FunctionDataModel

# Create your views here.

def viewData(request):

    function_data = FunctionDataModel.objects.all()

    context = {

        'function_data': function_data

    }

    return render(request, 'viewData/view.html', context)
