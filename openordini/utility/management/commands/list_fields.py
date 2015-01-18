import logging
from optparse import make_option
from django.core.management import BaseCommand
from open_municipio.acts.models import *
from django.db import models
from django.db.models import get_app, get_models
from django.db.models.loading import get_model
#from openordini.models import *

class Command(BaseCommand):
    """
    Elenco dei campi di un modello dati
    usa --m per indicare il nome dei modello
    """
    a = '<app ...>'
    m = '<model ...>'    
    help = "list fields of a model"

   
    option_list = BaseCommand.option_list + (
        make_option('-a', '--app', dest='app', help='App to exclude (use multiple --exclude to exclude multiple apps).'),
        make_option('-m', '--model', dest='model', help=('Copy templates to direcdory. (files '
                                          'are not oweritten if they exist).')),         
        )
    

    logger = logging.getLogger('webapp')

    def handle(self, *args, **options):
        """
        """
        fields = {}

        if options.get('app',False):
            self.stdout.write('opzione app:"%s"' %  options.get('app',False))
            app = get_app(options['app'])

        modello = options.get('model',[])
        if modello: 
            self.stdout.write('opzione modello:"%s"' %  options.get('model',[]))
            temp_model = get_model(options.get('app',False),modello)
            options = temp_model._meta
            for f in sorted(options.many_to_many + options.virtual_fields):
                print '%s: %s' % (f.name, f)  
            fields = temp_model._meta.get_all_field_names()
            for field in fields:
                self.stdout.write('campo:"%s"' % field)

       

        """
            for model in get_models(app):
                #new_object = model() # Create an instance of that model
                #model.objects.filter(...) # Query the objects of that model
                model._meta.db_table # Get the name of the model in the database
                model._meta.verbose_name # Get a verbose name of the model
                # ...
        """
        """        
            if args:
                options = args._meta
                fields = models.args._meta.get_all_field_names()
                print type(models.args._meta.get_all_field_names())
                for field in fields #sorted(options.concrete_fields + options.many_to_many + options.virtual_fields):
                    fields[field.name] = field
                    print field.name
                return fields        
            print "Nome, Email, DataIscrizione, DataUltimoLogin"
            for profile in profiles:
                print u'{u}, {u.email}, {u.date_joined}, {u.last_login}'.format(u=profile.user)
        """

  
