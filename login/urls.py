from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.mainLogin, name='mainLogin'),
    url(r'^newuser/$', views.newuser, name='newuser'),
    url(r'^success/$', views.success, name='success'),
    url(r'^logout/$', views.mainLogout, name='mainLogout')
]