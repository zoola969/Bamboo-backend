import re

from wtforms.validators import StopValidation

from bamboo.models import Client


class PhoneValidation(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        phone = str(field.data)

        try:
            Client().validate_phone('', phone)
        except AssertionError as e:
            if self.message is None:
                message = field.gettext(str(e))
            else:
                message = self.message

            field.errors[:] = []
            raise StopValidation(message)

