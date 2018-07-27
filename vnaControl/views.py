# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
#from .forms import *
import datetime
import sys
from .models import *
# PYMEASURE_ROOT=r'C:\ProgramData\Anaconda2\Lib\site-packages\pyMeasure'
# sys.path.append(PYMEASURE_ROOT)
# from Code.Analysis.Fitting import *
# from Code.DataHandlers.GraphModels import *
from pyMez import *
from pyMez.Code.Analysis.Fitting import *
from pyMez.Code.DataHandlers.GraphModels import *
from pyMez.Code.Analysis.Reports import *
import json
import matplotlib.pyplot as plt
import numpy as np
from fitting.models import FunctionDataModel, AcquisitionData
import traceback
import re


def default(request):
    return render(request, 'vnaControl/vna_control.html')


class VNAControl(TemplateView):

    template_name = "vnaControl/vna_control.html"

    is_vna_setup = False

    def post(self,request,**kwargs):

        print "VNA POST^^^^^^^^^^^^^^^^^"

        if not (request.user.is_authenticated()):
            print "########################################((((((((0203--3"
            return redirect('/login/') 

        form_id = str(request.POST.get('id'))
        output_dictionary = {}

        whos_there()

        vna = VNA("GPIB::16")

        if form_id == 'setupVNA':
            ifbw_value = int(request.POST.get('ifbw_value'))
            vna.set_IFBW(self, ifbw_value)

        return HttpResponse(json.dumps(output_dictionary))


    def get_context_data(self, **kwargs):
        print "VNA Context!!!!!!"
        context = super(VNAControl, self).get_context_data(**kwargs)

        return context

    def whos_there():
        """Whos_there is a function that prints the idn string for all
        GPIB instruments connected"""
        resource_manager = visa.ResourceManager()
        resource_list=resource_manager.list_resources()
        gpib_resources=[]
        gpib_idn_dictionary={}
        for instrument in resource_list:
            if re.search("GPIB",instrument,re.IGNORECASE):
                resource=resource_manager.open_resource(instrument)
                gpib_resources.append(resource)
                idn=resource.query("*IDN?")
                gpib_idn_dictionary[instrument]=idn
        if gpib_resources:
            for instrument_name,idn in gpib_idn_dictionary.iteritems():
                print("{0} is at address {1}".format(idn,instrument_name))
            print gpid_idn_dictionary
            return gpib_idn_dictionary
        else:
            print("There are no GPIB resources available")
            return None

# Create your views here.
