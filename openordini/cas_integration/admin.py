from django.contrib import admin

from .models import Capability

class CapabilityAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "link")
    list_filter = ["name", ]
    
    search_fields = ["user__first_name", "user__last_name", "user__email", "user__username", "name", "link", ]

admin.site.register(Capability, CapabilityAdmin)
