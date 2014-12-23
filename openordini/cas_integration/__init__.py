from django.utils.translation import ugettext as _

APP_LABEL = _("cas_integration")
APP_TITLE = _("Cas_Integration")


CAS_URI = 'http://localhost:8080/cas'
NSMAP = {'cas': CAS_URI}
CAS = '{%s}' % CAS_URI

def CAS_populate_user(user, authentication_response):

    print "raw response for user (%s): %s" % (user, authentication_response)

    if authentication_response.find(CAS + 'authenticationSuccess/'  + CAS + 'attributes'  , namespaces=NSMAP) is not None:
        attr = authentication_response.find(CAS + 'authenticationSuccess/'  + CAS + 'attributes'  , namespaces=NSMAP)

        if attr.find(CAS + 'is_superuser', NSMAP) is not None:
            user.is_superuser = attr.find(CAS + 'is_superuser', NSMAP).text.upper() == 'TRUE'

        if attr.find(CAS + 'is_staff', NSMAP) is not None:
            user.is_staff = attr.find(CAS + 'is_staff', NSMAP).text.upper() == 'TRUE'
