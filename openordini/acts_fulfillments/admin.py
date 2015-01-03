from django.contrib import admin
from django import forms
from django.forms import ModelForm
from .models import Fascicolo, InstitutionCharge


class CustomerInstitutionForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super(CustomerInstitutionForm, self).__init__(*args, **kwargs)
        wtf = InstitutionCharge.objects.filter();
        w = self.fields['recipient_set'].widget
        choices = []
        for choice in wtf:
            #choices.append((choice.id, choice.name))
            choices.append(choice.id)
        w.choices = choices

class FascicoloAdmin(admin.ModelAdmin):
    list_display = ("status", "approval_date", "publication_date","execution_date","initiative")

    filter_horizontal = ( "recipient_set", )
    search_fields = ["acts_support__support_type", "acts_support__support_date", ]
    filter_horizontal = ('recipient_set',)
    #form = CustomerInstitutionForm 

admin.site.register(Fascicolo, FascicoloAdmin)
