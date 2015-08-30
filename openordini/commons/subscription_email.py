from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.template.loader import render_to_string
from openordini.oo_email.models import recordo_login_by_email
from sendgrid.models import EmailMessage
import os
from smtplib import SMTPException
from email.mime.text import MIMEText as text
#from django.core.mail import send_mail
from django.dispatch import receiver
from sendgrid.signals import sendgrid_email_sent
from sendgrid.message import SendGridEmailMessage
from sendgrid.message import SendGridEmailMultiAlternatives

"""
Antonio, 29_08_2015
now, no loop but a single sending. So, User is the one we have selected 
"""

@receiver(sentgrid_email_sent)
def email_sended(sender, **kwargs):
    print "c e' nessuno... "	
    message = kwargs.get("message", None)
    #response = kwargs.get("response", None)
    #return message

class picked_email_to_send(): 
    m = email_sended # so i get the f or the return
    users_counter = 0
    def send_email_picked(self, profilo_utente_query):
        print profilo_utente_query
        self.stdout.write('testing  ... pick_email_to_send CLASS')
        print m.message
    
    
    emplate_base_path = os.path.join(settings.PROJECT_ROOT, 'templates/oo_users')
    email_txt_template_path = os.path.join(template_base_path, 'email.txt')
    email_html_template_path = os.path.join(template_base_path, 'email.html')
    
    #u = User.objects.get() #utente, utenti passati da admin  
    #if u.is_active or not u.is_active: # non ci interessa
    # TODO -> here we need to Know if a amail have been sent just to the current user
    # 
    #psicologo = User.objects.get(username=u.username)
    #mail_inviata = EmailMessage.objects.filter(to_email__contains = email)[0]
    #reg_test = recordo_login_by_email.objects.create(password_email=raw_password, username_email = u.username, utente_email = psicologo, ref_email = mail_inviata)
    #print "------------------------------------"
    
    #raw_password = User.objects.make_random_password(length=10)
        
        #-----------------------------------------
        #for u in User.objects.all().order_by("last_name").exclude(is_staff=True):
            #print "-------------------------------- test utenti"
            ##print vars(u)
            ##if not u.is_active:
            #if u.is_active or not u.is_active:
                # create a random string as password
                #raw_password = User.objects.make_random_password(length=10)

                # hash the "raw" password and assign it to the user
                #try:
                    #u.set_password(raw_password)
                    #u.is_active = True
                    #u.save()
                #except Exception as e:
                    #self.stdout.write('Error while assigning a password / activating the account of user "{0}" (pk={1}). No email will be sent to this user.'.format(u, u.pk))
                    #self.stdout.write('--> Error raised: {}'.format(e))
                    #continue

                # build the context that will be rendered in the email
                #email_context ={
                    #'username': u.username,
                    #'first_name': u.first_name,
                    #'last_name': u.last_name,
                    #'password': raw_password # the "raw" password (not encrypted!)
                #}

                # build the email for the user
                #print "Quale email usiamo %s" % (u.username)
                #email = u.email 
                #subject = 'Open Ordini - nuova password'
                #email_sender = 'stafgnpop@psicologipuglia.it' # TODO: replace this address with a meaningful one !
            
                #msg_text = render_to_string(email_txt_template_path, email_context)
                #msg_html = render_to_string(email_html_template_path, email_context)
                
                #self.stdout.write(msg_html)

                #if not email:
                    #email = 'vuota@vuota.it' 

                #msg = mail.EmailMultiAlternatives(subject, msg_text, email_sender, [email])
                #msg.attach_alternative(msg_html, 'text/html')

                #email_invio = SendGridEmailMultiAlternatives('Processo di informatizzazione NPOP', 'Nuovo Portale Ordine degli Piscologi... segue email per comunicarLe i dati di accesso', 'staff NPOP <stafgnpop@psicologipuglia.it>', [email])
                #email_invio.attach_alternative(msg_html, 'text/html')

                ###email_go = SendGridEmailMessage(subject, msg_html, email_sender, [email])

                # add the email to the list of emails that will be sent
                #self.stdout.write('Start sending emails to all the users ...')

                #connection = mail.get_connection(fail_silently=True) 

                #if options['users_limit']: 
                    #if users_counter >= options['users_limit']: 
                        #break
                #categories = ['credenziali','accesso']
                #if categories:
                
		    #logger.debug("Categories {c} were given".format(c=categories))
		    #The SendGrd Event API will POST different data for single/multiple category messages.
		    #if len(categories) == 1:
		        #email_invio.sendgrid_headers.setCategory(categories[0])
		    #elif len(categories) > 1:
		        #email_invio.sendgrid_headers.setCategory(categories)
		    #email_invio.update_headers()
                

