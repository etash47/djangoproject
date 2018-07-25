from django.conf.urls import url,include
from . import views
from .views import *
import re
operation_regex=re.compile('mean|med|all',re.IGNORECASE)

urlpatterns = [
    # url(r'^history/(?P<sample_name>\w+)/$', views.sample, name='sample'),
    # url(r'^instrument_control/(?P<sample_names>\w+)/$', view = KeithleyControl.as_view(), name = 'instrument_control'),
    # url(r'^instrument_control/(?P<template>[\w|-]+)/$',view=KeithleyControl.as_view(),name='instrument_control'),

    url(r'^$', views.default, name='default')
]
