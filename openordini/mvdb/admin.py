from django.contrib import admin
from .models import Regioni, Provincie, Comuni

class RegioniAdmin(admin.ModelAdmin):
    
    list_display = ("name", "slug", "codice_regione_istat")
    search_fields = ("name", "slug", "codice_regione_istat")

class ProvincieAdmin(admin.ModelAdmin):
    
    list_display = ("name", "slug", "codice_provincia_istat", "codice_regione_istat")
    search_fields = ("name", "slug", "codice_provincia_istat", "codice_regione_istat")
    list_filter = ["codice_regione_istat",]

class ComuniAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "codice_comune_istat", "codice_provincia_istat", "codice_alfanumerico_istat", "capoluogo_provincia", "capoluogo_regione")
    
    search_fields = ("name", "slug", "codice_comune_istat", "codice_provincia_istat", "codice_alfanumerico_istat")
    
    list_filter = ["codice_provincia_istat", "capoluogo_provincia", "capoluogo_regione",]

admin.site.register(Regioni, RegioniAdmin)
admin.site.register(Provincie, ProvincieAdmin)
admin.site.register(Comuni, ComuniAdmin)
