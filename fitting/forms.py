from django.forms import ModelForm
from .models import *


class FunctionForm(ModelForm):
    def Meta(self):
        model=FunctionDataModel
        fields = '__all__'

class DescriptionForm(ModelForm):
    def Meta(self):
        model=Description
        fields='__all__'

