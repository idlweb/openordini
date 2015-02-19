from django.contrib import admin
from django import forms
from django.forms import ModelForm
from django.db import models

from open_municipio.acts.admin import ActAdmin, TransitionInline, AttachInline

from .models import Fascicolo, InstitutionCharge, Act
from ..commons.widgets import AdvancedFilteredSelectMultiple


class FascicoloAdminForm(forms.ModelForm): 

    class Meta:
        widgets = {
            'recipient_set': AdvancedFilteredSelectMultiple("Recipients", is_stacked=True, attrs={'size':24})
        }

#class FascicoloAdmin(admin.ModelAdmin):
class FascicoloAdmin(ActAdmin):

    list_display = ("status", "approval_date", "publication_date","execution_date","initiative")
    search_fields = ["acts_support__support_type", "acts_support__support_date", ]

    # NB don't use filter_horizontal, otherwise it would "override" our customization
    # since the form uses FitleredSelectMultiple, it already includes the effect 
    # of flag "filter_horizontal"
    form = FascicoloAdminForm  

    inline_base = [ TransitionInline, AttachInline, ]    

admin.site.register(Fascicolo, FascicoloAdmin)
admin.site.unregister(Act)
