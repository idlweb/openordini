from django.contrib import admin

from open_municipio.data_import.models import Provider, LookupPerson, \
                                LookupAdministrationCharge, LookupCompanyCharge, \
                                LookupInstitutionCharge, FileImport
from open_municipio.idioticon.models import Term

# data import
admin.site.unregister(Provider)
admin.site.unregister(LookupPerson)
admin.site.unregister(LookupAdministrationCharge)
admin.site.unregister(LookupCompanyCharge)
admin.site.unregister(LookupInstitutionCharge)
admin.site.unregister(FileImport)
