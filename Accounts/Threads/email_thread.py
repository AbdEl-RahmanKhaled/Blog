import threading
from django.core.mail import EmailMessage


class EmailThread(threading.Thread):
    def __init__(self, email: EmailMessage):
        self.email = email
        super().__init__()

    def run(self):
        self.email.send()
