from django.conf.urls import patterns
from django.contrib import admin
from openordini.oo_email.models import recordo_login_by_email

class RecordoLoginByEmailAdmin(admin.ModelAdmin):
    list_display = ('username_email',)
    #list_filter = (VerificheListFilter,)
    search_fields = ["username_email", "utente_email__related_fieldname" ]
    #actions = ['validazione_casellario','export_come_JSON','export_selected_objects']

    
admin.site.register(recordo_login_by_email, RecordoLoginByEmailAdmin)
