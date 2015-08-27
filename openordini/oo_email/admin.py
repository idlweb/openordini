from django.conf.urls import patterns
from django.contrib import admin
from openordini.oo_email.models import recordo_login_by_email

class RecordoLoginByEmailAdmin(admin.ModelAdmin):
    model = recordo_login_by_email
    list_display = ('username_email', 'get_email',)

    def get_email(self, obj):
        return obj.utente_email.email
    
    #list_filter = (VerificheListFilter,)
    search_fields = ["username_email", ]
    #actions = ['validazione_casellario','export_come_JSON','export_selected_objects']
    

admin.site.register(recordo_login_by_email, RecordoLoginByEmailAdmin)
