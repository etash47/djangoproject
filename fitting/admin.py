# class functions from the standard library
import pyclbr
import re
import os
from django.contrib import admin

def register_all_models(module=None,path=None):
    """ This function registers all modules in with the django admin. 
    The module name should be a string, and defaults to 'models' and the path can be a string, list or tuple
    If you include the admin.ModelAdmin in the models.py module with the same name + Admin
    then it will register them too. Example if the model class is Pizza, then the admin model
    class would be PizzaAdmin """
    if module is None:
        module='models'
    if path is None:
        path=os.path.dirname(os.path.abspath(__file__))
        classes = pyclbr.readmodule(module,[path])
    elif type(path) is str:
        classes = pyclbr.readmodule(module,[path])
    else:
        classes = pyclbr.readmodule(module,path)
    # first make a list of string only parents
    for model in classes:
        if classes[model].super[0] in classes.values():
            classes[model].super=classes[model].super[0].super

    # make a list of admin classes
    admin_classes=[]
    for model in classes:
        for superclass in classes[model].super:
            try:
                if re.search('admin.ModelAdmin',superclass):
                    admin_classes.append(model)
            except:pass
    for model in classes:
        # now the dirty part, check that the models are classes that inherit from models.Model
        # if this inhertance is not explicit in the class call it will not be registered
        for superclass in classes[model].super:
            try:
                if re.search('models.Model',superclass):
                    try:
                        # Check to see if the modelNameAdmin is in the list of admin classes
                        test_name=model+'Admin'
                        if test_name in admin_classes:
                            exec('from %s import %s,%s'%(module,model,test_name))
                            exec('admin.site.register(%s,%s)'%(model,test_name))
                        else:
                        # this could be a from module import * above this loop
                            exec('from %s import %s'%(module,model))
                            exec('admin.site.register(%s)'%model)
                    except:raise
            except:pass
register_all_models()