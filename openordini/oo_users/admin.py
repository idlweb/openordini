from django.contrib import admin


from .models import UserProfile as OOUserProfile
from open_municipio.users.models import UserProfile as OMUserProfile

class UserProfileAdmin(admin.ModelAdmin):
    
    exclude = ("says_is_politician", )

# TODO try catch the unregister...
admin.site.unregister(OMUserProfile)
admin.site.register(OOUserProfile, UserProfileAdmin)
