from django.utils.log import AdminEmailHandler

from django.conf import settings
from django.core import mail
from django.views.debug import ExceptionReporter, get_exception_reporter_filter

class ManagerEmailHandler(AdminEmailHandler):
    """
    An exception log handler that emails log entries to site members
    of a group.    
    """

    def emit(self, record):
        """
        Taken from AdminEmailHandler.emit(...). The final part changes, because
        we want to send to addresses taken from settings.MANAGERS (instead of
        addresses taken from settings.ADMINS)
        """

#        print "record: %s" % record.__dict__

        try:
##            request = record.request
##            subject = '%s (%s IP): %s' % (
##                record.levelname,
##                ('internal' if request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS
##                 else 'EXTERNAL'),
##                record.getMessage()
##            )
##            filter = get_exception_reporter_filter(request)
##            request_repr = '\n{0}'.format(force_text(filter.get_request_repr(request)))

            subject = record.subject
        except Exception:
            subject = '%s: %s' % (
                record.levelname,
                record.getMessage()
            )
#            request = None
#            request_repr = "unavailable"
        subject = self.format_subject(subject)
        

        if record.exc_info:
            exc_info = record.exc_info
        else:
            exc_info = (None, record.getMessage(), None)

#        message = "%s\n\nRequest repr(): %s" % (self.format(record), request_repr)
        message = self.format(record)
        request = None
        reporter = ExceptionReporter(request, is_email=True, *exc_info)
        html_message = reporter.get_traceback_html() if self.include_html else None

        mail.mail_managers(subject, message, fail_silently=True,
                         html_message=html_message)

