from django.contrib import admin


from .models import Capability, GroupCapability

class CapabilityAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "link")
    list_filter = ["name", ]
    
    search_fields = ["user__first_name", "user__last_name", "user__email", "user__username", "name", "link", ]

class GroupCapabilityAdmin(admin.ModelAdmin):
    list_display = ("group", "name", "link")
    list_filter = ["group", "name", ]
    
    search_fields = ["group__name", "name", "link", ]



admin.site.register(Capability, CapabilityAdmin)
admin.site.register(GroupCapability, GroupCapabilityAdmin)
