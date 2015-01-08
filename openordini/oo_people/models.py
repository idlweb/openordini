from django.db import models

from open_municipio.people.models import Person

# Create your models here.

def get_current_institution_charges(self, moment=None):
    """
    Used to override the Person method with same name (the original method
    excludes committees)
    """
    return self.institutioncharge_set.select_related().current(moment=moment)

Person.get_current_institution_charges = get_current_institution_charges
Person.current_institution_charges = property(get_current_institution_charges)
