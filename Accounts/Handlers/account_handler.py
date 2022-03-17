import abc
from Accounts.models import Account
from validate_email import validate_email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from Accounts.utils import token_generator
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.html import strip_tags
from django.conf import settings
from Accounts.Threads.email_thread import EmailThread
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountHandler:
    __metaclass__ = abc.ABCMeta

    def __init__(self, request, account_obj: Account = None, first_name=None, last_name=None, username=None,
                 email=None, password=None, gender=None, credential=None, **kwargs):
        self.request = request
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password
        self.gender = gender
        self.__phone_number = ''
        self.account_obj = account_obj
        self.credential = credential

    def is_email_exist(self):
        return Account.objects.filter(email=self.email).exists()

    def is_username_exist(self):
        return Account.objects.filter(username=self.username).exists()

    def is_phone_exist(self):
        return Account.objects.filter(phone_number__contains=self.__phone_number).exists()

    def is_valid_email(self):
        print(self.email)
        return validate_email(self.email)

    def is_valid_password(self):
        return len(self.password) >= 6

    def is_valid_phone(self):
        return len(self.__phone_number) == 13

    def set_phone(self, phone):
        self.__phone_number = f'+2{phone}'

    def create_obj(self):
        self.account_obj = Account.objects.create_user(username=self.username,
                                                       email=self.email,
                                                       first_name=self.first_name,
                                                       last_name=self.last_name,
                                                       gender=self.gender,
                                                       phone_number=self.__phone_number)

    def send_email_verification(self):
        domain = get_current_site(self.request)
        mail_subject = 'Activate your account'
        html_content = get_template('accounts/email_forms/activate-account.html').render({
            'account': self.account_obj,
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(self.account_obj.pk)),
            'token': token_generator.make_token(self.account_obj)
        })
        mail_text = strip_tags(html_content)
        mail = EmailMultiAlternatives(subject=mail_subject, body=mail_text, from_email=settings.DEFAULT_FROM_EMAIL,
                                      to=[self.account_obj.email])
        mail.attach_alternative(html_content, 'text/html')

        # mail = EmailMessage(subject=mail_subject,
        #                     body=mail_body,
        #                     from_email=settings.DEFAULT_FROM_EMAIL,
        #                     to=[self.account_obj.email])
        EmailThread(mail).start()

    def request_rest_password(self):
        valid = False
        if self.is_email_exist():
            domain = get_current_site(self.request)
            account = Account.objects.filter(email__iexact=self.email)[0]
            mail_subject = 'Reset your password'
            html_content = get_template('accounts/email_forms/rest-password.html').render({
                'account': account,
                'domain': domain,
                'uid': urlsafe_base64_encode(force_bytes(account.pk)),
                'token': PasswordResetTokenGenerator().make_token(account)
            })
            # mail_body = render_to_string('accounts/email_forms/rest-password.html', )
            mail_text = strip_tags(html_content)
            # mail = EmailMessage(subject=mail_subject,
            #                     body=mail_body,
            #                     from_email=settings.DEFAULT_FROM_EMAIL,
            #                     to=[account.email])

            mail = EmailMultiAlternatives(subject=mail_subject, body=mail_text, from_email=settings.DEFAULT_FROM_EMAIL,
                                          to=[account.email])
            mail.attach_alternative(html_content, 'text/html')
            EmailThread(mail).start()
            valid = True
        return valid

    def change_password(self):
        done = False
        if self.is_valid_password():
            self.account_obj.set_password(self.password)
            self.account_obj.save()
            done = True
        return done

    def auth_credential(self):
        if '@' in self.credential:
            return {'email': self.credential}
        else:
            return {'username': self.credential}

    @abc.abstractmethod
    def is_valid_account(self):
        pass

    @abc.abstractmethod
    def register(self):
        pass

    @abc.abstractmethod
    def is_authorized(self):
        pass
    #
    # @abc.abstractmethod
    # def login(self):
    #     pass

    # @abc.abstractmethod
    # def validate_fields(self):
    #     pass
