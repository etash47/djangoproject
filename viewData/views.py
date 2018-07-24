# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from fitting.models import FunctionDataModel, AcquisitionData

# Create your views here.

def viewData(request):

    function_data = FunctionDataModel.objects.all()
    acquisition_data = AcquisitionData.objects.all()

    context = {

        'function_data': function_data,
        'acquisition_data': acquisition_data,

    }

    return render(request, 'viewData/view.html', context)
