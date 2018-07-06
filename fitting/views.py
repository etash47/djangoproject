# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
from .forms import *
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
import re


# Create your views here.

def interpolation(request):
    return render(request, 'fitting/interpolation.html')


def run_application(request):
    if not (request.user.is_authenticated()):
        return redirect('/login/')
    return render(request, 'fitting/not_index.html')



def index(request):
    print "########################################(((((((("

    if not (request.user.is_authenticated()):
        return redirect('/login/')  

    now=datetime.datetime.now()
    html="<html><body><h1>The time is {0}</h1></body></html>".format(now)
    return HttpResponse(html)
# def create_measurement_download_link(xml_data_table):
#     download_nodes=["ExcelFile","Csv","Ods","MatFile"]
#     mime_types=["","text/plain","",""]
#     table_graph=TableGraph()
#     table_graph.set_state("Xml")

class NotIndex(TemplateView):

    template_name = "fitting/not_index.html"
    def post(self,request,**kwargs):
        if not (request.user.is_authenticated()):
            print "########################################((((((((1-0101"
            return redirect('/login/')  

        print("{0} is {1}".format("request.POST",request.POST))
        #print("{0} is {1}".format("request.POST.get('fname')",request.POST.get('fname')))
        print("{0} is {1}".format("dir(request)",dir(request)))
        print("{0} is {1}".format("request.read()",request.read()))
        output_dictionary = {}
        equation=str(request.POST.get('equation'))
        variables = str(request.POST.get('variables'))
        parameters = str(request.POST.get('parameters'))
        x_min=float(request.POST.get('x_min'))
        x_max=float(request.POST.get('x_max'))
        plot_format=str(request.POST.get('format'))
        number_points=int(request.POST.get('numberPoints'))
        entry_dictionary={"equation_text":equation,"variables":variables,
                          "parameters":parameters,"x_min":x_min,"x_max":x_max,"number_points":number_points}
        new_function=FunctionDataModel(**entry_dictionary)
        new_function.save()

        name='duh'
        context=self.get_context_data(name=name)
        # right here I am rendering the response instead of just sending an HttpResponse
        try:
            f=FunctionalModel(variables=variables,parameters=parameters,equation=equation)
            parameter_dict={}
            for parameter in f.parameters[:]:
                parameter_dict[parameter]=float(request.POST.get(parameter))
            f.set_parameters(**parameter_dict)
            #data=DataSimulator(model=f,output_noise_type='normal',output_noise_center=0,output_noise_width=20)
            #data.set_x(x_min,x_max,number_points)
            #f.clear_parameters
            figure=plt.figure()
            x_data=np.linspace(x_min,x_max,number_points)
            # y_data=[2*x**2+3 for x in x_data]
            plt.plot(x_data,f(x_data),plot_format,label="${0}$".format(sympy.latex(f.equation)))
            plt.title("${0}$".format(f.to_latex()))
            plt.legend()
            graph=ImageGraph()
            graph.set_state('MatplotlibFigure',figure)
            graph.move_to_node("EmbeddedHtml")
            context['content']=graph.data
            graph.move_to_node('Base64')
            base_64=graph.data
            graph_name=re.sub('[\W]+|[*]|[-]|[+]',"_",equation)
            context["download_link"]="<a href='data:image/png;base64,{0}' download = '{1}.png'>Download Image</a>".format(base_64,graph_name)

            output_dictionary["content"]=context['content']
            output_dictionary["download_link"]=context['download_link']
        except:
            raise
            print("There was an exception")
            pass

        return HttpResponse(json.dumps(output_dictionary))

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(NotIndex, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['content']=""
        context['download_link']="Nothing to dowload yet"
        context['time']=datetime.datetime.utcnow()
        return context

class FittingNext(NotIndex):
    template_name = "fitting/fitting_next.html"

class KeithleyControl(TemplateView):
    """Class that allows the view of keithley data"""
    template_name = "fitting/instrument_control.html"

    def post(self,request,**kwargs):

        if not (request.user.is_authenticated()):
            print "########################################((((((((0203--3"
            return redirect('/login/')  

        form_id=str(request.POST.get('id'))
        output_dictionary = {}
        if form_id == 'fitData':
            print("{0} is {1}".format("request.POST", request.POST))
            # print("{0} is {1}".format("request.POST.get('fname')",request.POST.get('fname')))
            print("{0} is {1}".format("dir(request)", dir(request)))
            print("{0} is {1}".format("request.read()", request.read()))

            equation = str(request.POST.get('equation'))
            variables = str(request.POST.get('variables'))
            parameters = str(request.POST.get('parameters'))
            x_min = float(request.POST.get('x_min'))
            x_max = float(request.POST.get('x_max'))
            plot_format = str(request.POST.get('format'))
            number_points = int(request.POST.get('numberPoints'))
            entry_dictionary = {"equation_text": equation, "variables": variables,
                                "parameters": parameters, "x_min": x_min, "x_max": x_max,
                                "number_points": number_points}
            new_function = FunctionDataModel(**entry_dictionary)
            new_function.save()

            name = 'duh'
            context = self.get_context_data(name=name)
            # right here I am rendering the response instead of just sending an HttpResponse
            try:
                last_data = Measurement.objects.last()
                xml_data = DataTable(None,content=last_data.measurement_content)
                f = FunctionalModel(variables=variables, parameters=parameters, equation=equation)
                parameter_dict = {}
                for parameter in f.parameters[:]:
                    parameter_dict[parameter] = float(request.POST.get(parameter))
                f.set_parameters(**parameter_dict)
                # data=DataSimulator(model=f,output_noise_type='normal',output_noise_center=0,output_noise_width=20)
                # data.set_x(x_min,x_max,number_points)
                # f.clear_parameters
                figure = plt.figure()
                x_data = np.linspace(x_min, x_max, number_points)
                # y_data=[2*x**2+3 for x in x_data]
                plt.plot(xml_data.to_list("Voltage"),xml_data.to_list("Current"),label=last_data.measurement_name)
                plt.plot(x_data, f(x_data), plot_format, label="Initial Guess ${0}$".format(f.to_latex()))
                f.fit_data(np.array(map(lambda x:float(x),xml_data.to_list("Voltage"))),
                           np.array(map(lambda x:float(x),xml_data.to_list("Current"))))
                plt.plot(x_data, f(x_data), plot_format, label="Fit ${0}$".format(f.to_latex()))
                plt.title("${0}$".format(f.to_latex()))
                plt.legend()
                graph = ImageGraph()
                graph.set_state('MatplotlibFigure', figure)
                graph.move_to_node("EmbeddedHtml")
                context['fit_content'] = graph.data
                graph.move_to_node('Base64')
                base_64 = graph.data
                graph_name = re.sub('[\W]+|[*]|[-]|[+]', "_", equation)
                context[
                    "fit_download_link"] = "<a href='data:image/png;base64,{0}' download = '{1}.png'>Download Image</a>".format(
                    base_64, graph_name)

                output_dictionary["fit_content"] = context['fit_content']
                output_dictionary["fit_download_link"] = context['fit_download_link']
            except:
                raise
                print("There was an exception")
                pass
        elif form_id == 'takeData':
            # start the experiment
            experiment=KeithleyIV()
            # retrieve the values from the form on the template
            v_min=float(request.POST.get('vMin'))
            v_max=float(request.POST.get('vMax'))
            number_points=int(request.POST.get('numberPoints'))
            bowtie=bool(request.POST.get('bowtie'))
            notes=str(request.POST.get('notes'))
            sample_name=str(request.POST.get('sampleName'))
            plot_format = str(request.POST.get('format'))
            # generate the voltage list
            voltage_list=experiment.make_voltage_list(v_min,v_max,number_points=number_points,bowtie=bowtie)
            # extra crap to make it work, need to fix for real
            settling_time=.2
            name="name"
            context = self.get_context_data(name=name)
            output_dictionary={}
            instrument_avaible=True
            try:
                experiment.initialize_keithley()
                experiment.take_IV(voltage_list, settle_time=settling_time)
            except:
                instrument_avaible=False
                text = 'Entering fake mode, keithley did not respond fake R=12000.1'
                print text
                fake_list = voltage_list
                for index, voltage in enumerate(fake_list):
                    current = voltage / 12000.1
                    experiment.data_list.append({'Index': index, 'Voltage': voltage, 'Current': current})
            # plot do not call plt.show()!!
            figure=plt.figure()
            voltage_list = []
            current_list = []
            for data in experiment.data_list:
                voltage_list.append(float(data['Voltage']))
                current_list.append(float(data['Current']))
            plt.plot(voltage_list, current_list,plot_format)
            plt.xlabel("Voltage (V)")
            plt.ylabel("Current (A)")
            # UDT to EmbeddedHTML for plot
            graph = ImageGraph()
            graph.set_state('MatplotlibFigure', figure)
            graph.move_to_node("EmbeddedHtml")
            context['content'] = graph.data
            # UDT and add to a link
            graph.move_to_node('Base64')
            base_64 = graph.data
            graph_name = "IV"
            context["download_link"] = "<a href='data:image/png;base64,{0}' download = '{1}.png'>Download Image</a>".format(
                base_64, graph_name)
            output_dictionary["content"] = context['content']
            output_dictionary["download_link"] = context['download_link']
            # Create a measurement and state and store in the database
            experiment.calculate_resistance()
            data_dictionary={}
            data_dictionary['Data_Description'] = {'Current': 'Current in Amps',
                                                        'Voltage': 'Voltage in Volts',
                                                        'Index': 'Order in which the point was taken',
                                                        'Instrument_Description': KEITHLEY_INSTRUMENT_SHEET,
                                                        'Date': datetime.datetime.utcnow().isoformat(),
                                                        'Notes': notes, 'Name': sample_name,
                                                        'Resistance': str(experiment.resistance)}
            data_dictionary['Data'] = experiment.data_list
            if instrument_avaible:
                state =InstrumentState(None, state_dictionary=experiment.instrument.get_state(),
                                                                         style_sheet=os.path.join(TESTS_DIRECTORY,
                                                                             "../XSL/DEFAULT_STATE_STYLE.xsl"))
                state.append_description(
                    description_dictionary={"Instrument_Description": KEITHLEY_INSTRUMENT_SHEET})

                data_dictionary["Data_Description"]["State"] = "./" + state.path
                new_state = InstrumentState(state_content=str(state), state_name=state.path)
                new_state.save()
                download_state = String_to_DownloadLink(str(state),
                                                        mime_type="text/xml-application",
                                                        suggested_name=state.path,
                                                        text="xml")

                # now transform the measurements to different formats
                link_options = {"nodes": ['XmlFile', 'CsvFile', 'HtmlFile', 'JsonFile'],
                                "extensions": ['xml', 'csv', 'html', 'json'],
                                "mime_types": ['application/xml', 'text/plain',
                                               'text/html', 'application/json']}
                state_table = [[ key, value.replace("\n", "")] for key, value in state.state_dictionary.iteritems()]
                state_ascii=AsciiDataTable(None,data=state_table,column_names=["Set","Value"])
                print("{0} is {1}".format("state_table",state_table))
                print("{0} is {1}".format("state_xml", state_ascii))
                table_graph = TableGraph()
                table_graph.set_state("AsciiDataTable", state_ascii)
                extra_links = TableGraph_to_Links(table_graph, base_name=new_state.path,**link_options)
                output_dictionary["state_download_link"] = download_state+" || state downloads -> " + extra_links
            measurement_data = DataTable(None, data_dictionary=data_dictionary,
                                                                          style_sheet=os.path.join(TESTS_DIRECTORY,
                                                                              "../XSL/DEFAULT_MEASUREMENT_STYLE.xsl"))
            new_measurement=Measurement(measurement_content=str(measurement_data),measurement_name=measurement_data.path)

            new_measurement.save()

            # Add a set of links
            download_measurement=String_to_DownloadLink(str(measurement_data),
                                                        mime_type="text/xml-application",
                                                        suggested_name=measurement_data.path,
                                                        text="xml")

            # now transform the measurements to different formats
            table_graph=TableGraph()
            table_graph.set_state("XmlDataTable",measurement_data)

            ##### So that I can remember the nodes
            # {"base_name": None,
            #     "nodes": ['XmlFile', 'CsvFile', 'ExcelFile', 'OdsFile', 'MatFile', 'HtmlFile', 'JsonFile'],
            #     "extensions": ['xml', 'csv', 'xlsx', 'ods', 'mat', 'html', 'json'],
            #     "mime_types": ['application/xml', 'text/plain',
            #                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            #                    'application/vnd.oasis.opendocument.spreadsheet',
            #                    'application/x-matlab-data', 'text/html', 'application/json']}

            link_options={"nodes": ['XmlFile', 'CsvFile', 'HtmlFile', 'JsonFile'],
             "extensions": ['xml', 'csv', 'html', 'json'],
             "mime_types": ['application/xml', 'text/plain',
                            'text/html', 'application/json']}
            extra_links=TableGraph_to_Links(table_graph,base_name=measurement_data.path,**link_options)

            # excel and text formats
            output_dictionary["measurement_download_link"]=download_measurement+" || table downloads -> " + extra_links


        return HttpResponse(json.dumps(output_dictionary))

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(KeithleyControl, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['content']=""
        context['time']=datetime.datetime.utcnow()
        context['download_link']="Nothing to dowload yet"
        return context

class Index(TemplateView):
    """A basic view that links the template named index.html in home/templates to the view."""
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        """Defines the context data passed to the template. To create a named variable
        either put a named regex (?P<variable_name>) in the url pattern that links to this view
        or add context['variable_name']=value in this method"""
        context= super(Index, self).get_context_data(**kwargs)
        return context
