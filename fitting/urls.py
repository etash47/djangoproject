from django.conf.urls import url,include
from .views import *
import re
operation_regex=re.compile('mean|med|all',re.IGNORECASE)

urlpatterns = [
    url(r'^$',view=Index.as_view(),name='index'),
    url('^plot(?P<template>[\w|-]+)/$',view=NotIndex.as_view(),name='not_index'),
    url('^a(?P<template>[\w|-]+)/$',view=FittingNext.as_view(),name='fitting_next'),
    url('^(?P<template>(?i)(mean|med|all))/$',view=Index.as_view(),name='index'),
    url('^(?P<template>[\w|-]+)/$',view=KeithleyControl.as_view(),name='instrument_control'),
]