from .account_handler import AccountHandler
from django.contrib import auth


class ViewsAccountHandler(AccountHandler):
    def is_valid_account(self):
        errors = []
        is_valid = True
        if not self.is_valid_email():
            is_valid = False
            errors.append('This email is not valid')

        if self.is_email_exist():
            is_valid = False
            errors.append('This email is already exist')

        if self.is_username_exist():
            is_valid = False
            errors.append('Username is taken')

        if self.is_phone_exist():
            is_valid = False
            errors.append('This Phone Number is already exist')

        if not self.is_valid_password():
            is_valid = False
            errors.append('The password must be more than or equal 6 characters')

        if not self.is_valid_phone():
            is_valid = False
            errors.append('Phone number is not valid')

        return is_valid, errors

    def register(self):
        is_valid, errors = self.is_valid_account()

        if is_valid:
            self.create_obj()
            self.account_obj.set_password(self.password)
            self.account_obj.save()
            self.send_email_verification()
        return is_valid, errors

    def is_authorized(self):
        pass
