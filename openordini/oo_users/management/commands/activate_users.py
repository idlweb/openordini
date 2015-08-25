from optparse import make_option

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core.management.base import NoArgsCommand, CommandError
from django.template.loader import render_to_string
from openordini.oo_email.models import recordo_login_by_email
import os

#import smtplibu
from smtplib import SMTPException
from email.mime.text import MIMEText as text
#from django.core.mail import send_mail
from sendgrid.message import SendGridEmailMessage
from sendgrid.message import SendGridEmailMultiAlternatives


class Command(NoArgsCommand):

    help = 'Assign random password to all the users in the DB and send an email (with the uncrypted password) to each of them.'
    option_list = NoArgsCommand.option_list + (
        make_option('--dryrun', action='store_true', dest='dryrun', help='Deny email sending (print them in the console)'),
        make_option('--limit', type='int', dest='users_limit', help='Limit the number of users activated (and emails sent)'),
    )

  
    def handle_noargs(self, **options):
        
        def html_escape(text):  
            text = text.replace('&', '&amp;')
            text = text.replace('"', '&quot;')
            text = text.replace("'", '&#39;')
            text = text.replace(">", '&gt;') 
            text = text.replace("<", '&lt;')
            text = text.replace(u"\uFFFD", "?")
            return text

        self.stdout.write('Start assigning random passwords to the users and building one email for each of them ...')

        email_list = []
        
        template_base_path = os.path.join(settings.PROJECT_ROOT, 'templates/oo_users')
        
        email_txt_template_path = os.path.join(template_base_path, 'email.txt')
        email_html_template_path = os.path.join(template_base_path, 'email.html')

        users_counter = 0

        #-----------------------------------------
                        
        #-----------------------------------------
           
        """
        Isolo il blocco massivo
        if email_list:
            print "numero email da inviare %s" % (len(email_list))
            print "email inviate %s" %(users_counter)
            self.stdout.write('Start sending emails to all the users ...')

            if options['dryrun']:
                # don't actually send any email
                connection = mail.get_connection(backend='django.core.mail.backends.console.EmailBackend')
            else:
                # use default email connection
                connection = mail.get_connection(fail_silently=True)
            print "-------------------------------- invio emails"
            # vars(email_list)
            # send all the emails in a single call, using a single connection
            try:
                connection.send_messages(email_list) 
                print "Successfully sent email"
            except SMTPException: 
                print "Error: unable to send email" 
        """
