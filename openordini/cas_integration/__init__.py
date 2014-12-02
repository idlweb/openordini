
CAS_URI = 'http://www.yale.edu/tp/cas'
NSMAP = {'cas': CAS_URI}
CAS = '{%s}' % CAS_URI

def CAS_populate_user(user, authentication_response):
    from .models import Capability


    print "raw response for user (%s): %s" % (user, authentication_response)

    if authentication_response.find(CAS + 'authenticationSuccess/'  + CAS + 'attributes'  , namespaces=NSMAP) is not None:
        attr = authentication_response.find(CAS + 'authenticationSuccess/'  + CAS + 'attributes'  , namespaces=NSMAP)

        if attr.find(CAS + 'is_superuser', NSMAP) is not None:
            user.is_superuser = attr.find(CAS + 'is_superuser', NSMAP).text.upper() == 'TRUE'

        if attr.find(CAS + 'is_staff', NSMAP) is not None:
            user.is_staff = attr.find(CAS + 'is_staff', NSMAP).text.upper() == 'TRUE'

    # TODO parameterize these urls
    for g in user.groups.all():
        capability, created = Capability.objects.get_or_create(user=user, name="weblog", link="http://cms.psicologipuglia.it/%s/" % g.name)
    capability, created = Capability.objects.get_or_create(user=user, name="profile", link="http://oo.psicologipuglia.it/users/profile/%s/" % user.username)

    print "user cap (%s): %s" % (type(user), user.capabilities)
