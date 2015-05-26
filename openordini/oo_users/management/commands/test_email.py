from optparse import make_option

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core.management.base import NoArgsCommand, CommandError
from django.template.loader import render_to_string

import os

class Command(NoArgsCommand):

    help = 'test invio email'
   
    def handle_noargs(self, **options):

        self.stdout.write('invio diretto')

        email_list = []
        template_base_path = os.path.join(settings.PROJECT_ROOT, 'templates/oo_users')
        email_txt_template_path = os.path.join(template_base_path, 'email.txt')
        email_html_template_path = os.path.join(template_base_path, 'email.html')

        users_counter = 0

        # build the email for the user
        recipients_list = ['antonio.vangi.av@gmail.com', 'francesco.spegni@gmail.com']
        subject = 'invio email di test'
        email_sender = 'stafgnpop@psicologipuglia.it' # TODO: replace this address with a meaningful one !

        email_context ={
            'first_name': 'tonio',
            'last_name': 'npop',
            'password': 'test' # the "raw" password (not encrypted!)
        }
            
        msg_text = render_to_string(email_txt_template_path, email_context)
        msg_html = render_to_string(email_html_template_path, email_context)

        msg = mail.EmailMultiAlternatives(subject, msg_text, email_sender, recipients_list)

        msg.attach_alternative(msg_html, 'text/html')

        # add the email to the list of emails that will be sent
        email_list.append(msg)


        if email_list:
            self.stdout.write('Start sending emails to all the users ...')
            # use default email connection
            connection = mail.get_connection()
            self.stdout.write("Connection: %s" % connection)
            # send all the emails in a single call, using a single connection
            connection.send_messages(email_list)
