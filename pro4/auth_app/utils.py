from django.core.mail import send_mail
import threading

class SendEmail:
    @staticmethod
    def send_email_to_user(subject,message,from_email,recipient_list):
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False
        )
        
class EmailThread(threading.Thread):
    def __init__(self,subject,message,from_email,recipient_list):
        self.subject = subject
        self.message = message
        self.from_email = from_email
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)
        super().__init__()
        
    def run(self) -> None:
        SendEmail.send_email_to_user(self.subject,self.message,self.from_email,self.recipient_list)