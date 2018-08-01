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

S2P_TEST_FILE_PATH=os.path.join(TESTS_DIRECTORY,"thru.s2p")

def default(request):
    return render(request, 'vnaControl/vna_control.html')


class VNAControl(TemplateView):
    """Uses a django server to acquire data from a vna. The vna gpib address has been hardcoded
    in for now, as whos_there() causes an unknown error on certain computers. """
    VNA_ADDRESS="GPIB::20"
    template_name = "vnaControl/vna_control.html"

    is_vna_setup = False

    def post(self,request,**kwargs):

        print("VNA POST Has been triggered at {0}".format(datetime.datetime.now()))
        print("The request dictionary is {0}".format(request.POST.dict()))

        if not (request.user.is_authenticated()):
            print "########################################((((((((0203--3"
            return redirect('/login/') 

        form_id = str(request.POST.get('id'))

        # we respond with output dictionary, it is turned to a json object which is then
        # read when the request in the rendered template has changed state
        #  if (this.readyState == 4 && this.status == 200) says do this if the response is valid
        #  the var response = JSON.parse(this.responseText) is the response on the client side
        output_dictionary = {}

        #whos_there()

        # if we are posting, create a vna and decide what setup is needed
        # Right now designed for the RS in 4639

        try:
            vna = VNA(self.VNA_ADDRESS)
            vna_found = True
        except:
            print("There was no VNA found at {0} entering testing mode".format(self.VNA_ADDRESS))
            vna=FakeInstrument(self.VNA_ADDRESS)
            vna_found=False


        if form_id=='ParameterSelectionForm':
            if vna_found:
                vna.initialize()
            else:
                vna.write("Initialization occured here")
            output_dictionary["initialized"]="VNA initialized"

        elif form_id=='VNASetupForm':
            vna.write("SENS:BAND {0}".format(request.POST.get("IFBW")))
            if bool(request.POST.get("CorrectionOn")):
                vna.write("SENS:CORR:STAT {0}".format(1))
            else:
                vna.write("SENS:CORR:STAT {0}".format(0))

        elif form_id=='freqSweepForm':
            type_sweep = request.POST.get("sweepType")
            start = float(request.POST.get("sweepStart"))
            stop = float(request.POST.get("sweepStop"))
            number_points = int(request.POST.get("numberPoints"))
            if vna_found:
                vna.set_frequency(start=start,stop=stop,number_points=number_points,type=type_sweep)
            else:
                vna.write("start {0}, stop {1},number points {2} ,type {3}".format(start,stop,number_points,type_sweep))

        elif form_id=='takeData':
            if vna_found:

                s2p=vna.measure_sparameters()
            else:
                s2p=S2PV1(S2P_TEST_FILE_PATH)

            sample_name=request.POST.get("sampleNameInput")
            notes=request.POST.get("notesInput")
            connector_type=request.POST.get("ConnectorType")
            s2p.add_comment("Device_Id = {0}".format(sample_name))
            s2p.add_comment("Measurement_Connector_Type = {0}".format(connector_type))
            s2p.add_comment("Notes = {0}".format(notes))
            figure=s2p.show(silent=True)

            image_graph=ImageGraph()
            image_graph.set_state(node_name="MatplotlibFigure",node_data=figure)
            image_graph.move_to_node("EmbeddedHtml")
            image_link=image_graph.data
            #image_graph.jump_to_external_node(external_node_name="Thumbnail")
            #thumbnail=image_graph.data
            #image_graph.set_state(node_name="Jpg", node_data=thumbnail)
            #image_graph.move_to_node("EmbeddedHtml")
            #thumbnail_link=image_graph
            html_report=HTMLReport()
            html_report.add_toggle_style()
            html_report.add_toggle_style()
            #html_report.add_toggle(tag_id="instrument")
            try:
                instrument_description=vna.to_HTML(XSLT=os.path.join(TESTS_DIRECTORY,
                                                                  "../XSL/DEFAULT_INSTRUMENT_STYLE.xsl"))
            except:
                instrument_description="<h3> No Instrument Description Available</h3>"


            html_report.embedd_image(image=figure,imsge_mode="MatplotlibFigure")
            html_report+HTMLBase(html_text=instrument_description)
            output_dictionary["thumbnailDisplay"]=image_link.replace("<img","<img width='500px'")
            s2p.change_data_format("RI")
            xml_s2p=SNP_to_XmlDataTable(s2p)
            html=xml_s2p.to_HTML(XSLT=os.path.join(TESTS_DIRECTORY,"../XSL/S2P_RI_STYLE.xsl"))

            output_dictionary["interactiveView"]=String_to_DownloadLink(str(html),
                                                        mime_type="text/html-application",
                                                        suggested_name=change_extension(s2p.path,".html"),
                                                        text="Interactive Data")
            output_dictionary["measurementDownload"]=String_to_DownloadLink(str(s2p),
                                                        mime_type="text",
                                                        suggested_name=s2p.path,
                                                        text="s2p")
            state=InstrumentState(None,state_dictionary=vna.get_state())
            state_html=state.to_HTML(XSLT=os.path.join(TESTS_DIRECTORY,"../XSL/DEFAULT_STATE_STYLE.xsl"))

            output_dictionary["stateDownload"]=String_to_DownloadLink(str(state),
                                                        mime_type="text/xml-application",
                                                        suggested_name=state.path,
                                                        text="State")
            html_report=html_report+HTMLBase(html_text=state_html)+HTMLBase(html_text=html)

            output_dictionary["completeDownload"]=String_to_DownloadLink(str(html_report),
                                                        mime_type="text/html-application",
                                                        suggested_name=html_report.path,
                                                        text="Report")


        return HttpResponse(json.dumps(output_dictionary))


    def get_context_data(self, **kwargs):
        print("The get_context_data method of the {0} template was called".format(self.template_name))
        context = super(VNAControl, self).get_context_data(**kwargs)
        try:
            vna = VNA(self.VNA_ADDRESS)
            vna_found = True
            context["connection"] = "connected to"
        except:
            print("There was no VNA found at {0} entering testing mode".format(self.VNA_ADDRESS))
            vna=FakeInstrument(self.VNA_ADDRESS)
            vna_found=False
            context["connection"]="emulating"
        context["vna_idn"]=vna.idn
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
