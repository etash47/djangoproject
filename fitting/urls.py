from django.conf.urls import url,include
from . import views
from .views import *
import re
operation_regex=re.compile('mean|med|all',re.IGNORECASE)

urlpatterns = [

    url(r'^instrument_control/equation_id=(?P<id>\d+)/$', views.equation, name='equation'),

    url(r'^not_index/', view = NotIndex.as_view(), name = 'not_index'),
    url(r'^fitting_next/', view = FittingNext.as_view(), name = 'fitting_next'),
    url(r'^index/', view = Index.as_view(), name = 'index'),
    url(r'^instrument_control/', view = KeithleyControl.as_view(), name = 'instrument_control'),

    url(r'^$',view=Index.as_view(),name='index'),
    url(r'^plot(?P<template>[\w|-]+)/$',view=NotIndex.as_view(),name='not_index'),
    url(r'^fitting_next/a(?P<template>[\w|-]+)/$',view=FittingNext.as_view(),name='fitting_next'),
    url(r'^index/(?P<template>(?i)(mean|med|all))/$',view=Index.as_view(),name='index'),
    url(r'^instrument_control/(?P<template>[\w|-]+)/$',view=KeithleyControl.as_view(),name='instrument_control'),

    url(r'^interpolation/$', views.interpolation, name='interpolation')
]