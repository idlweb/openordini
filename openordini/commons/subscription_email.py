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
from sendgrid.models import EmailMessage
from sendgrid.signals import sendgrid_email_sent
from sendgrid.message import SendGridEmailMessage
from sendgrid.message import SendGridEmailMultiAlternatives

"""
Antonio, 29_08_2015
now, no loop but a single sending. So, User is the one we have selected 
"""


class picked_email_to_send: 
    # so i get the f or the return
    #actually it's wrong recall the function, upon, i must get the assignment ... m = email_sended() 
    def send_email_picked(self, qs):
        users_counter = 0
        print qs
        print('testing  ... pick_email_to_send CLASS')
        
        template_base_path = os.path.join(settings.PROJECT_ROOT, 'templates/oo_users')
        email_txt_template_path = os.path.join(template_base_path, 'email.txt')
        email_html_template_path = os.path.join(template_base_path, 'email.html')
        
        for u in qs:#User.objects.all().order_by("last_name").exclude(is_staff=True):
            print u.user
            # email gia' inviate 
            # se trovo una email non devo mandarne un'altra
            ei = EmailMessage.objects.filter(to_email = u.user.email)
            print "email corrente"
            print u.user.email
            print "quanto e' ei"
            print ei
            if ei.count() < 1:
            	print ------------------- ENTRATO
	        # create a random string as password
	        raw_password = User.objects.make_random_password(length=10)
	        # hash the "raw" password and assign it to the user
		try:
		    u.user.set_password(raw_password)
		    u.user.is_active = True
		    u.user.save()
		except Exception as e:
		    #self.stdout.write('Error while assigning a password / activating the account of user "{0}" (pk={1}). No email will be sent to this user.'.format(u, u.pk))
		    #self.stdout.write('--> Error raised: {}'.format(e))
		    continue
	
	            # build the context that will be rendered in the email
	            print u.user.first_name
	        email_context ={
	            'username': u.user.username,
	            'first_name': u.user.first_name,
	            'last_name': u.user.last_name,
	            'password': raw_password # the "raw" password (not encrypted!)
	        }
	
	        # build the email for the user
	        #print "Quale email usiamo %s" % (u.username)
	        email = u.user.email 
	        subject = 'Open Ordini - nuova password'
	        email_sender = 'stafgnpop@psicologipuglia.it' # TODO: replace this address with a meaningful one !
	        msg_text = render_to_string(email_txt_template_path, email_context)
	        msg_html = render_to_string(email_html_template_path, email_context)
	    
	        if not email:
	            email = 'vuota@vuota.it' 
	    
	        email_invio = SendGridEmailMultiAlternatives('Processo di informatizzazione NPOP', 'Nuovo Portale Ordine degli Piscologi... segue email per comunicarLe i dati di accesso', 'staff NPOP <stafgnpop@psicologipuglia.it>', [email])
	        email_invio.attach_alternative(msg_html, 'text/html')
	 
	        categories = ['credenziali','accesso']
	        if categories:
	            #logger.debug("Categories {c} were given".format(c=categories))
	            #The SendGrd Event API will POST different data for single/multiple category messages.
	            if len(categories) == 1:
	               email_invio.sendgrid_headers.setCategory(categories[0])
		    elif len(categories) > 1:
		        email_invio.sendgrid_headers.setCategory(categories)
		    email_invio.update_headers()
		    
		try:                    
	            #email_list.append(msg)
	            email_invio.send()
	            #psicologo = User.objects.get(username=u.username)
	            #mail_inviata = EmailMessage.objects.filter(to_email__contains = email)[0]
	            #reg_test = recordo_login_by_email.objects.create(password_email=raw_password, username_email = u.username, utente_email = psicologo, ref_email = mail_inviata)
	   
	                
	        except SMTPException: 
	                print "Error: unable to send email" 
	                continue
                
        
    @receiver(sendgrid_email_sent)
    def email_sended(sender, **kwargs):
        print "c e' nessuno... "	
        message = kwargs.get("message", None)
        print message
        #response = kwargs.get("response", None)
        #return message
    
 
    
    # TODO -> here we need to Know if a amail have been sent just to the current user
    # 
    #psicologo = User.objects.get(username=u.username)
    #mail_inviata = EmailMessage.objects.filter(to_email__contains = email)[0]
    #reg_test = recordo_login_by_email.objects.create(password_email=raw_password, username_email = u.username, utente_email = psicologo, ref_email = mail_inviata)
    #print "------------------------------------"
    
    #raw_password = User.objects.make_random_password(length=10)
        
        #-----------------------------------------
        #       

