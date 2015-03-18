from django.conf import settings

from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from django.contrib.auth.models import User, Group
from django.db import transaction

from registration.models import RegistrationProfile

from adaptor.model import CsvModel
from adaptor.fields import IntegerField
from .fields import OOCsvCharField, OOCsvBooleanField, OOCsvDateField, \
                    OOCsvFloatField

from open_municipio.people.models import Person, Institution, InstitutionCharge
from openordini.oo_users.models import UserProfile, ExtraPeople, Recapito

import logging

logger = logging.getLogger("import")

def update_or_create(model, **kwargs):
    """
    This is equivalent to the method with the same name introduced in Django 1.7
    """

    defaults = kwargs.pop("defaults", {})

    obj, created = model.objects.get_or_create(defaults=defaults, **kwargs)

    if not created and defaults:
        for key,value in defaults.iteritems():
            setattr(obj, key, value)
      
        obj.save()

    return (obj, created)


# the mapping has the following format:
#
# [csv field name] -> [model field spec]
#
# [model field spec] is either:
# - a tuple (app name, model name): it is subsumed that the field name is the 
#   same as the csv field name
# - a tuple (app name, model name, field name): in case the model field is different from
#   the csv field name
# - a list of tuples (app name, model name) or (app name, model name, field name): in case the same
#   csv field contribute to multiple field in one or multiple models

MAP_CSV_FIELDS_TO_MODELS = {
    "email": "auth.user",
    "username": "auth.user",
    "first_name": [ "auth.user", "people.person" ],
    "last_name": [ "auth.user", "people.person" ],

    "birth_date": "people.person",
    "birth_location": "people.person",
    "sex": "people.person",

    "is_psicologo_clinico": ("oo_users.userprofile", "says_is_psicologo_clinico"),
    "is_psicologo_lavoro": ("oo_users.userprofile", "says_is_psicologo_lavoro"),
    "is_psicologo_forense": ("oo_users.userprofile", "says_is_psicologo_forense"),
    "is_dottore_tecniche_psicologiche": ("oo_users.userprofile", "says_is_dottore_tecniche_psicologiche"),
    "is_asl_employee": ("oo_users.userprofile", "says_is_asl_employee"),
    "is_self_employed": ("oo_users.userprofile", "says_is_self_employed"),
    "register_subscription_date": "oo_users.userprofile",
    "numero_iscrizione": "oo_users.userprofile",

    "indirizzo_residenza": "oo_users.extrapeople",
    "citta_residenza": "oo_users.extrapeople",
    "cap_residenza": "oo_users.extrapeople",
    "provincia_residenza": "oo_users.extrapeople",
    "indirizzo_domicilio": "oo_users.extrapeople",
    "citta_domicilio": "oo_users.extrapeople",
    "cap_domicilio": "oo_users.extrapeople",
    "provincia_domicilio": "oo_users.extrapeople",
    "indirizzo_studio": "oo_users.extrapeople",
    "citta_studio": "oo_users.extrapeople",
    "cap_studio": "oo_users.extrapeople",
    "provincia_studio": "oo_users.extrapeople",
    "denominazione_studio": "oo_users.extrapeople",
    "coord_lat": "oo_users.extrapeople",
    "coord_long": "oo_users.extrapeople",
    "codice_fiscale": "oo_users.extrapeople",
    "accertamento_casellario": "oo_users.extrapeople",
    "accertamento_universita": "oo_users.extrapeople",

    "tel_residenza": "oo_users.recapito",
    "tel_domicilio": "oo_users.recapito",
    "tel_ufficio": "oo_users.recapito",
    "tel_cellulare": "oo_users.recapito",
    "indirizzo_pec": "oo_users.recapito",
    "sito_internet": "oo_users.recapito",
    "consegna_corrispondenza": "oo_users.recapito",
    
    "ritiro_agenda": "oo_users.caratteristiche_gestione",
    "invio_tesserino": "oo_users.caratteristiche_gestione",
    "numero_faldone": "oo_users.caratteristiche_gestione",

    "trasferimento_data": "oo_users.trasferimento",
    "delibera_trasferimento": "oo_users.trasferimento",
    "motivazione_trasferimento": "oo_users.trasferimento",
    "regione_trasferimento": "oo_users.trasferimento",
    "tassa_trasferimento": "oo_users.trasferimento",

    "titolo_laurea": "oo_users.psicologo_titoli",
    "articolo_tre": "oo_users.psicologo_titoli",
    "articolo_tre_delibera": "oo_users.psicologo_titoli",
    "articolo_tre_data": "oo_users.psicologo_titoli",
    "articolo_tre_note": "oo_users.psicologo_titoli",
    "laurea_specializzazione": "oo_users.psicologo_titoli",
}

class Command(BaseCommand):

    args = '<file1 file2 ...>'
    help = 'Import user information from the passed file'

    # TODO parameterize this (pass via command line, add a default value in the settings)
    send_user_activation_email = False

    group_cache = {}
    institution_cache = {}

    def populate_cache(self):
    
        groups = Group.objects.all()

        for g in groups:
            self.group_cache[g.name] = g
    
        institutions = Institution.objects.all()

        for i in institutions:
            self.institution_cache[i.slug] = i

    def handle(self, *args, **options):
            
        logger.info("Start importing user data ...")


        num_read = 0
        num_write = 0
        num_files = 0
        tot_files = len(args)

        self.populate_cache()

        for file in args:

            logger.info("Reading user data from file: %s ..." % file)
            try:
                data = self.parse(file)
                num_files = num_files + 1
            except Exception, e:
                logger.exception(e)
                logger.warning("Error reading file: %s. Details: %s. Continue with next..." % (file, e))
                continue

            for curr_data in data:

                num_read = num_read + 1 
                
                try:
    
                    self.save_row(curr_data)
   
                    num_write = num_write + 1

                except Exception, e:

                    logger.exception(e)
                    logger.warning("Error importing user and related data: %s. Continue with next one ..." % e)

        logger.info("Finished importing user data. Total files: %s. Files parsed: %s. Total users: %s. Users imported: %s" % (tot_files, num_files, num_read, num_write))

    @transaction.commit_on_success
    def save_row(self, curr_data):
        logger.debug("Save person ...")
        person = self.save_person(curr_data)

        assert person != None

        logger.debug("Save user ...")
        user = self.save_inactive_user(curr_data, p=person)

        assert user != None

        logger.debug("Save user profile ...")
        profile = self.save_user_profile(curr_data, u=user, p=person)

        logger.debug("Save extra profile ...")
        extra = self.save_extra(curr_data, up=profile)

        logger.debug("Save contacts ...")
        recapito = self.save_recapito(curr_data, up=profile)

        # TODO salvataggio titoli, trasferimento, gestione ?

        logger.debug("Save charges ...")
        self.save_charges(curr_data, p=person, u=user, up=profile, e=extra)
 

    def parse(self, file):
        """
        read the file and return a list of user data
        """

        grouped_data = []

        # TODO handle filesystem problems
        data = UserCsvModel.import_data(data = open(file))

        for row in data:
            group = {}

            group = self.group_data(row)

            grouped_data.append(group)

        return grouped_data

    def group_data(self, row):

        group = {}

        for csv_field,spec in MAP_CSV_FIELDS_TO_MODELS.iteritems():

            # first, normalize spec to be always a list
            if not isinstance(spec, list):
                spec = [ spec ]

            for curr_spec in spec:

                if isinstance(curr_spec, tuple):
                    full_name = curr_spec[0]
                    model_field = curr_spec[1]
                elif isinstance(curr_spec, basestring):
                    full_name = curr_spec
                    model_field = csv_field
                else:
                    raise Exception("Wrong format for field specification. Expected string or tuple")
            
                if not full_name in group:
                    group[full_name] = {}

                group[full_name][model_field] = getattr(row, csv_field)
    
        return group


    def save_person(self, curr_data):
        """
        save an instance of model Person
        """

        f = curr_data["people.person"]

        p, created = update_or_create(Person,
            first_name = f["first_name"],
            last_name = f["last_name"],
            birth_date = f["birth_date"],
            defaults=f)

        if not created:
            logger.info("Person %s already exists. Update it ..." % p)

        return p

        return None

    def save_inactive_user(self, curr_data, p):
        """
        Save an inactive user, and takes care of sending the activation email.
        """

        assert isinstance(p, Person)

        f = curr_data["auth.user"]
        f["is_active"] = False
        f["is_staff"] = False
        f["is_superuser"] = False

        username = f.get("username", None)

        if not username:
            while True:
                # generate a random username and check it is unique
                username = User.objects.make_random_password(length=8) # TODO generate a random one
                if User.objects.filter(username=username).count() == 0:
                    break

        password = f.get("password", None)
        if not password:
            password = User.objects.make_random_password(length=10)

        email = f["email"]


        user,created = update_or_create(User, username=username,email=email,defaults=f)

        if not created:
            logger.info("User '%s' (email '%s') already exists. Update id ..." % (username, email))
        

        if self.send_user_activation_email:
            # TODO send the customized email
            pass

        return user

    def save_user_profile(self, curr_data, u, p):

        assert isinstance(u, User)
        assert isinstance(p, Person)

        f = curr_data["oo_users.userprofile"]        
    
        f["user"] = u
        f["person"] = p

        logger.debug("User profile data: %s" % (f,))

        up, created = update_or_create(UserProfile, user=u, defaults=f)

        if not created:
            logger.info("User profile for user '%s' already exists. Update it ..." % u)

        return up

    def save_extra(self, curr_data, up):

        assert isinstance(up, UserProfile)

        f = curr_data["oo_users.extrapeople"]

        f["anagrafica_extra"] = up

        e, created = update_or_create(ExtraPeople, anagrafica_extra=up,
                            defaults=f)

        if not created:
            logger.info("Extra information already present for user '%s'. Update it ..." % up)

        return e

    def save_recapito(self, curr_data, up):

        assert isinstance(up, UserProfile)

        f = curr_data["oo_users.recapito"]
        f["recapiti_psicologo"] = up

        r, created = update_or_create(Recapito, recapiti_psicologo=up, 
                        defaults=f)

        if not created:
            logger.info("Contacts information for user '%s' already present. Update it ..." % up)

        return r

    def save_charges(self, curr_data, p, u, e, up):

        assert isinstance(p, Person)
        assert isinstance(u, User)
        assert isinstance(up, UserProfile)
        assert isinstance(e, ExtraPeople)

        says_is_psicologo_clinico = up.says_is_psicologo_clinico
        says_is_psicologo_lavoro = up.says_is_psicologo_lavoro
        says_is_psicologo_forense = up.says_is_psicologo_forense
        says_is_dottore_tecniche_psicologiche = up.says_is_dottore_tecniche_psicologiche
        register_subscription_date = up.register_subscription_date

        is_registered_a = (register_subscription_date != None) and (says_is_psicologo_lavoro or says_is_psicologo_clinico or says_is_psicologo_forense)

        charges = []

        if is_registered_a:
            self.save_institution_charge(p=p, institution_slug=settings.SYSTEM_GROUP_NAMES["sezione_a"], date=register_subscription_date, charges=charges)

        if says_is_psicologo_lavoro:
            self.save_user_group(u=u, group_name=settings.SYSTEM_GROUP_NAMES["psicologo_lavoro"])

        if says_is_psicologo_clinico:
            self.save_user_group(u=u, group_name=settings.SYSTEM_GROUP_NAMES["psicologo_clinico"])

        if says_is_psicologo_forense:
            self.save_user_group(u=u, group_name=settings.SYSTEM_GROUP_NAMES["psicologo_forense"])

        is_registered_b = (register_subscription_date != None) and (says_is_dottore_tecniche_psicologiche)

        if is_registered_b:
            self.save_institution_charge(p=p, institution_slug=settings.SYSTEM_GROUP["sezione_b"], date=register_subscription_date, charges=charges)

        if says_is_dottore_tecniche_psicologiche:
            self.save_user_group(u=u, group_name=settings.SYSTEM_GROUP_NAMES["dottore_tecniche_psicologiche"])

        return charges
        

    def save_institution_charge(self, p, date, institution_slug, charges):
        i = self.institution_cache[institution_slug]
        member_charge = InstitutionCharge.objects.create(person=p, institution=i, start_date=date)

        charges.append(member_charge)
   

    def save_user_group(self, u, group_name):

        assert isinstance(u, User)

        g = self.group_cache[group_name]
        assert isinstance(g, Group)
        
        g.user_set.add(u)



class UserCsvModel(CsvModel):
    email = OOCsvCharField(null=True)
    username = OOCsvCharField(null=True)
    first_name = OOCsvCharField()
    last_name = OOCsvCharField()
    birth_date = OOCsvDateField(format=settings.IMPORT_DATE_FORMAT)
    birth_location = OOCsvCharField(null=True,default="")
    sex = OOCsvBooleanField()
    is_psicologo_clinico = OOCsvBooleanField(null=True,default=False)
    is_psicologo_lavoro = OOCsvBooleanField(null=True,default=False)
    is_psicologo_forense = OOCsvBooleanField(null=True,default=False)
    is_dottore_tecniche_psicologiche = OOCsvBooleanField(null=True,default=False)
    is_asl_employee = OOCsvBooleanField(null=True,default=False)
    is_self_employed = OOCsvBooleanField(null=True,default=False)
    register_subscription_date = OOCsvDateField(format=settings.IMPORT_DATE_FORMAT, null=True)
    numero_iscrizione = IntegerField(null=True, default=0)
    indirizzo_residenza = OOCsvCharField(null=True,default="")
    citta_residenza = OOCsvCharField(null=True,default="")
    cap_residenza = OOCsvCharField(null=True,default="",limit=5)
    provincia_residenza = OOCsvCharField(null=True,default="")
    indirizzo_domicilio = OOCsvCharField(null=True,default="")
    citta_domicilio = OOCsvCharField(null=True,default="")
    cap_domicilio = OOCsvCharField(null=True,default="",limit=5)
    provincia_domicilio = OOCsvCharField(null=True,default="")
    indirizzo_studio = OOCsvCharField(null=True,default="")
    citta_studio = OOCsvCharField(null=True,default="")
    cap_studio = OOCsvCharField(null=True,default="",limit=5)
    provincia_studio = OOCsvCharField(null=True,default="")
    denominazione_studio = OOCsvCharField(null=True,default="")
    coord_lat = OOCsvFloatField(null=True)
    coord_long = OOCsvFloatField(null=True)
    codice_fiscale = OOCsvCharField(null=True,default="")
    accertamento_casellario = OOCsvBooleanField(null=True,default=False)
    accertamento_universita = OOCsvBooleanField(null=True,default=False)
    tel_residenza = OOCsvCharField(null=True,default="")
    tel_domicilio = OOCsvCharField(null=True,default="")
    tel_ufficio = OOCsvCharField(null=True,default="")
    tel_cellulare = OOCsvCharField(null=True,default="")
    indirizzo_pec = OOCsvCharField(null=True,default="")
    sito_internet = OOCsvCharField(null=True,default="")
    consegna_corrispondenza = OOCsvCharField(null=True,default="") #{ residenza, domicilio, studio }
    ritiro_agenda = OOCsvBooleanField(null=True,default=False)
    invio_tesserino = OOCsvBooleanField(null=True,default=False)
    numero_faldone = OOCsvCharField(null=True,default="")
    trasferimento_data = OOCsvDateField(format=settings.IMPORT_DATE_FORMAT, null=True)
    delibera_trasferimento = OOCsvCharField(null=True,default="")
    motivazione_trasferimento = OOCsvCharField(null=True,default="")
    regione_trasferimento = OOCsvCharField(null=True,default="")
    tassa_trasferimento = OOCsvFloatField(null=True)
    titolo_laurea = OOCsvCharField(null=True,default="")
    articolo_tre = OOCsvBooleanField(null=True,default=False)
    articolo_tre_delibera = OOCsvCharField(null=True,default="")
    articolo_tre_data = OOCsvDateField(format=settings.IMPORT_DATE_FORMAT, null=True)
    articolo_tre_note = OOCsvCharField(null=True,default="")
    laurea_specializzazione = OOCsvBooleanField(null=True,default=False)

    class Meta:
        has_header = True
        delimiter = ","
