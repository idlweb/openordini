from django.contrib import admin
from django import forms

from .models import UserProfile as OOUserProfile
from openordini.oo_users.models import ExtraPeople, Recapito, Caratteristiche_gestione, Trasferimento, PsicologoTitoli

from open_municipio.users.models import UserProfile as OMUserProfile
from django.utils.translation import ugettext_lazy as _

from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers

from django.contrib.contenttypes.models import ContentType


class UserProfileAdmin(admin.ModelAdmin):    
    exclude = ("says_is_politician", )
    


""" ERRORE richiesta id"""
class UserInline(admin.TabularInline):
    model = OOUserProfile


""" blocco funzionante A3"""
def upper_case_name(obj):
    return ("%s, %s" % (obj.indirizzo_email, obj.indirizzo_pec)).upper() 
upper_case_name.short_description = 'riferimento recapito'



#@admin.register(Recapito)
class RecapitoAdmin(admin.ModelAdmin):
    #fields = (('tel_cellulare', 'indirizzo_email'), 'indirizzo_pec')
    list_display = ('tel_cellulare', 'indirizzo_email', 'indirizzo_pec')
    list_filter = ('recapiti_psicologo__person__last_name','recapiti_psicologo__person__first_name')
    #list_display = (upper_case_name,) #A3
    #inlines = [
    #    UserInline
    #]
    pass


""" 
Query personalizzata Verifiche
"""
class VerificheListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('verifiche')
     # Parameter for the filter that will be used in the URL query.
    parameter_name = 'verifiche'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('casellario', _('casellario da verificare')),
            ('titolo', _('titoli non verificati')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'casellario':
            return queryset.filter(accertamento_casellario=False)
        if self.value() == 'titolo':
            return queryset.filter(accertamento_universita=False)     





class ExtraPeopleAdmin(admin.ModelAdmin):
    list_filter = (VerificheListFilter,)
    search_fields = ["anagrafica_extra__person__last_name", ]        
    
    actions = ['validazione_casellario','export_come_JSON','export_selected_objects']

    def validazione_casellario(self, request, queryset):
        rows_updated = queryset.update(accertamento_casellario=True)
        if rows_updated == 1:
            message_bit = "Una scheda aggiornata"
        else:
            message_bit = "%s schede sono state" % rows_updated
        self.message_user(request, "%s correttamente modificate." % message_bit)
        
    validazione_casellario.short_description = "validazione del casellario"

    def export_come_JSON(self, request, queryset):
        response = HttpResponse(content_type="application/json")
        serializers.serialize("json", queryset, stream=response)
        return response

    def export_selected_objects(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))


""" 
Query personalizzata Specializzazioni
"""
class SpecializzatiListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('specializzati')
     # Parameter for the filter that will be used in the URL query.
    parameter_name = 'specializzati'
    def lookups(self, request, model_admin):       
        return (
            ('articolo 3', _('specializzati presenti')),
        )
    def queryset(self, request, queryset):
        if self.value() == 'articolo 3':
            return queryset.filter(articolo_tre=True)
 

""" 
Query personalizzata filtrando il REQUEST
"""
class AuthSpecializzatiListFilter(SpecializzatiListFilter):
    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            return super(AuthSpecializzatiListFilter,
                self).lookups(request, model_admin)

    def queryset(self, request, queryset):
        if request.user.is_superuser:
            return super(AuthSpecializzatiListFilter,
                self).queryset(request, queryset)     


class MyPsicologoTitoAdminForm(forms.ModelForm):
    def clean_titolo(self):
        # do something that validates your data
        return self.cleaned_data["titolo_laurea"]


class PsicologoTitoliAdmin(admin.ModelAdmin):
    list_filter = (AuthSpecializzatiListFilter,)
    search_fields = ["titolo_laurea", ]
    form = MyPsicologoTitoAdminForm
    pass




# TODO try catch the unregister...
admin.site.unregister(OMUserProfile)
admin.site.register(OOUserProfile, UserProfileAdmin)
admin.site.register(ExtraPeople, ExtraPeopleAdmin)
admin.site.register(Recapito, RecapitoAdmin)
admin.site.register(Caratteristiche_gestione)
admin.site.register(Trasferimento)
admin.site.register(PsicologoTitoli, PsicologoTitoliAdmin)