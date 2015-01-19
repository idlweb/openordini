import logging
from optparse import make_option
from django.core.management import BaseCommand
from open_municipio.acts.models import *
from django.db import models
from django.db.models import get_app, get_models
from django.db.models.loading import get_model
from django.conf import settings

#from openordini.models import *

class Command(BaseCommand):
    """
    """   
    help = "list fields of a model"

   
    option_list = BaseCommand.option_list + (
        make_option('-a', '--app', dest='app', help='.'),
        )
    

    logger = logging.getLogger('webapp')

    def handle(self, *args, **options):
        """
        """
        
        print(settings.INSTALLED_APPS)     

        


  
