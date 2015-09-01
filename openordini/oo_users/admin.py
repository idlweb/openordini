from django.conf.urls import patterns
from django.contrib import admin
from django import forms

from .models import UserProfile as OOUserProfile
from .models import ExtraPeople, Recapito, Caratteristiche_gestione, Trasferimento, PsicologoTitoli

from open_municipio.users.models import UserProfile as OMUserProfile
from django.utils.translation import ugettext_lazy as _

from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers

from django.contrib.contenttypes.models import ContentType
from suit.widgets import SuitDateWidget, SuitTimeWidget, SuitSplitDateTimeWidget

from ajax_changelist.admin import AjaxModelAdmin

from .regbackend import finalize_registration
from .forms import CustomAjaxModelFormView 
from django.contrib.auth.models import User, Group

from openordini.commons import subscription_email 


#from django.utils.html import escape



"""
Query personalizzata Verifiche
"""
class emailBusinessListFilter(admin.SimpleListFilter):
    title = _('consenso email')
    parameter_name = 'verifica consenso'

    def lookups(self, request, model_admin):
        return (
            ('1', _('consenso dato')),
            ('0', _('consenso non dato')),
            #('titolo', _('consenso non espresso')),
        )

    def queryset(self, request, queryset):

        if self.value() == '1':
            queryset = queryset.filter(wants_commercial_newsletter=True)
        elif self.value() == '0':
            queryset = queryset.filter(wants_commercial_newsletter=False)

        return queryset

class CustomAjaxModelAdmin(AjaxModelAdmin):

    def __init__(self, *args, **kwargs):

        # 'post_callback' (if it's used) must be defined as one of the options
        # on the subclass of this class
        if not hasattr(self, 'post_callback'):
            self.post_callback = None

        super(CustomAjaxModelAdmin, self).__init__(*args, **kwargs)


    def get_urls(self):
        """Full overriding of the parent's method.

        Avoid duplicating this url pattern by defining it ONLY here.
        (the 'super()' called here actually skips one level of class hierarchy).
        """
        urls = super(AjaxModelAdmin, self).get_urls()
        list_urls = patterns('',
                (r'^(?P<object_id>\d+)$',
                 CustomAjaxModelFormView.as_view(model=self.model,
                                            valid_fields=self.ajax_list_display,
                                            post_callback=self.post_callback)))
        return list_urls + urls


class UserProfileAdmin(CustomAjaxModelAdmin):
    ajax_list_display = ('numero_iscrizione',)
    post_callback = finalize_registration
    exclude = ("says_is_politician", )
    search_fields = ["person__last_name", "person__first_name"]
    list_display = ('person','wants_commercial_newsletter','email_login_inviata')
    list_filter =(emailBusinessListFilter,)
    actions = ['send_email_on_selection','send_email_on_selection_false',]
    
    def send_email_on_selection(self, request, queryset):
        ioc = subscription_email.picked_email_to_send()
        print "NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNrisultato della funzione"
       
        t_email = ioc.send_email_picked(queryset)
        print t_email 
        
        if t_email == True:
            rows_updated = queryset.update(email_login_inviata=True)
        else:
            rows_updated = queryset.update(email_login_inviata=False)
            
        if rows_updated == 1:
            message_bit = "email inviata"
        else:
            message_bit = "%s email inviate" % rows_updated
        self.message_user(request, "%s email inviate." % message_bit)

    send_email_on_selection.short_description = "Invia email psicologi selezionati"
    
    def send_email_on_selection_false(self, request, queryset):
        #ioc = subscription_email.picked_email_to_send()
        #ioc.send_email_picked(queryset)

        rows_updated = queryset.update(email_login_inviata=False)
        if rows_updated == 1:
            message_bit = "campo azzerato"
        else:
            message_bit = "%s email azzerate" % rows_updated
        self.message_user(request, "%s email azzerate." % message_bit)
        
    send_email_on_selection_false.short_description = "deseleziona invio email"
    
    
    def save_model(self, request, obj, form, change):             
        up = self.model
        if obj.id: #and up.objects.get(id = obj.id).exists():
           print "verificata l'esistenza del profilo personale"
           u = up.objects.get(id = obj.id)
           finalize_registration(self, u)  
        obj.save()
      

""" ERRORE richiesta id"""
#class UserInline(admin.TabularInline):
#    model = OOUserProfile


""" blocco funzionante A3"""
def upper_case_name(obj):
    return ("%s, %s" % (obj.indirizzo_email, obj.indirizzo_pec)).upper()
upper_case_name.short_description = 'riferimento recapito'



#@admin.register(Recapito)
class RecapitoAdmin(admin.ModelAdmin):
    #fields = (('tel_cellulare', 'indirizzo_email'), 'indirizzo_pec')
    list_display = ('recapiti_psicologo','tel_cellulare', 'indirizzo_email', 'indirizzo_pec', )
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
    title = _('verifiche')
    parameter_name = 'verifiche'

    def lookups(self, request, model_admin):
        return (
            ('casellario', _('casellario da verificare')),
            ('titolo', _('titoli non verificati')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'casellario':
            return queryset.filter(accertamento_casellario=False)
        if self.value() == 'titolo':
            return queryset.filter(accertamento_universita=False)





class ExtraPeopleAdmin(admin.ModelAdmin):
    list_display = ('anagrafica_extra','accertamento_casellario','accertamento_universita')
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
    title = _('specializzati')
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


#Non funziona
#class PsicologoTitoliForm(forms.ModelForm):
#    class Meta:
#        model = PsicologoTitoli
#        widgets = {
#            'data_iscrizione_albo': SuitSplitDateTimeWidget,
#        }


class MyPsicologoTitoliAdminForm(forms.ModelForm):
    def clean_titolo(self):
        # do something that validates your data
        return self.cleaned_data["titolo_laurea"]


class PsicologoTitoliAdmin(admin.ModelAdmin):
    list_filter = (AuthSpecializzatiListFilter,)
    search_fields = ["titolo_laurea", ]
    form = MyPsicologoTitoliAdminForm
    pass


"""
   A subclass of this admin will let you add buttons (like history) in the
   change view of an entry.
"""
class ButtonableModelAdmin(admin.ModelAdmin):

   buttons=[]

   def change_view(self, request, object_id, extra_context={}):
      extra_context['buttons']=self.buttons
      return super(ButtonableModelAdmin, self).change_view(request, object_id, extra_context)

   def __call__(self, request, url):
      if url is not None:
         import re
         res=re.match('(.*/)?(?P<id>\d+)/(?P<command>.*)', url)
         if res:
            if res.group('command') in [b.func_name for b in self.buttons]:
               obj = self.model._default_manager.get(pk=res.group('id'))
               getattr(self, res.group('command'))(obj)
               return HttpResponseRedirect(request.META['HTTP_REFERER'])

      return super(ButtonableModelAdmin, self).__call__(request, url)



# TODO try catch the unregister...
admin.site.unregister(OMUserProfile)
admin.site.register(OOUserProfile, UserProfileAdmin)
admin.site.register(ExtraPeople, ExtraPeopleAdmin)
admin.site.register(Recapito, RecapitoAdmin)
admin.site.register(Caratteristiche_gestione)
admin.site.register(Trasferimento)
admin.site.register(PsicologoTitoli, PsicologoTitoliAdmin)
