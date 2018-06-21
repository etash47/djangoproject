from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User,Group
import datetime
import json

from django.db import models
from django.core.serializers.json import DjangoJSONEncoder


class JSONField(models.TextField):
    """
    JSONField is a generic textfield that neatly serializes/unserializes
    JSON objects seamlessly.
    Django snippet #1478

    example:
        class Page(models.Model):
            data = JSONField(blank=True, null=True)


        page = Page.objects.get(pk=5)
        page.data = {'title': 'test', 'type': 3}
        page.save()
    """

    def to_python(self, value):
        if value == "":
            return None

        try:
            if isinstance(value, str):
                return json.loads(value)
        except ValueError:
            pass
        return value

    def from_db_value(self, value, *args):
        return self.to_python(value)

    def get_db_prep_save(self, value, *args, **kwargs):
        if value == "":
            return None
        if isinstance(value, dict):
            value = json.dumps(value, cls=DjangoJSONEncoder)
        return value

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    today=datetime.date.today()
    return 'files/{0}/{1}/{2}/{3}/{4}'.format(instance.owner.get_username(), today.year,today.month,today.day,filename)
# Create your models here.

class TestModel(models.Model):
    """A test model"""
    comment=models.CharField(max_length=100)
    number=models.FloatField()
class ArbitraryFile(models.Model):
    "Just a model that holds the string representation of a file"
    string=models.TextField(verbose_name="String data",name="string")
    def __str__(self):
        return "String data number {0}".format(self.pk)

class Measurement(models.Model):
    """Holds the string value and name of a measurement"""
    content=models.TextField(name="measurement_content")
    name=models.CharField(max_length=500,name="measurement_name")
    def __str__(self):
        return self.measurement_name

class State(models.Model):
    "holds the content and name of an instrument state"
    content=models.TextField(name="state_content")
    name=models.CharField(max_length=500,name="state_name")
    def __str__(self):
        return self.state_name


class FunctionDataModel(models.Model):
    "Stores the information needed to make a FunctionalModel"
    equation_text=models.CharField(max_length=500)
    parameters=models.CharField(max_length=500)
    variables=models.CharField(max_length=200)
    x_min=models.FloatField()
    x_max=models.FloatField()
    number_points=models.IntegerField()

    def __str__(self):
        return self.equation_text

class Entity(models.Model):
    """The model for a user entered file, in general anything to be described"""
    owner=models.ForeignKey(User,verbose_name="User who added the file",name="owner")
    file = models.FileField(upload_to=user_directory_path,verbose_name="File Model",name="file")
    location = models.CharField('Location on Disk', max_length=500,null=True,default="A fake location")
    time_added=models.DateTimeField(verbose_name="Time File Added",name="time_added",auto_now_add=True)
    def __str__(self):
        return self.file.name


class FloatValue(models.Model):
    value=models.FloatField(null=True)
    def __str__(self):
        return self.value
class IntValue(models.Model):
    value=models.IntegerField(null=True)
    def __str__(self):
        return self.value

class TextValue(models.Model):
    value=models.TextField(null=True)
    def __str__(self):
        return self.value

class pyMeasureKnowledgeSystem(models.Model):
    property=models.CharField(max_length=500,null=True)
    property_units=models.CharField(max_length=500,null=True)
    property_description=models.CharField(max_length=500,null=True)
    property_type=models.CharField(max_length=500,null=True)
    def __str__(self):
        return self.property

class Description(models.Model):
    """A set of descriptions of the enities"""
    entity=models.ForeignKey(Entity)
    float_value=models.ForeignKey(FloatValue,null=True, blank=True,)
    int_value=models.ForeignKey(IntValue,null=True, blank=True,)
    text_value=models.ForeignKey(TextValue,null=True, blank=True,)
    pyMeasure_ks=models.ForeignKey(pyMeasureKnowledgeSystem,null=True, blank=True,)
    def __str__(self):
        return "{0} : {1}".format(self.entity.file.name,self.pk)

class Project(models.Model):
    project_name=models.CharField(name="name",max_length=500)
    project_wall=models.TextField(name="wall",null=True,blank=True)
    project_descriptions=models.ManyToManyField(Description,name="descriptions",null=True,blank=True)
    project_groups=models.ManyToManyField(Group,null=True,blank=True)
    def __str__(self):
        return self.name


