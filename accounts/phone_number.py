import phonenumbers
from django.core.exceptions import ValidationError
from django.db import models


class PhoneNumberField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 20)
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        try:
            parsed_number = phonenumbers.parse(value, 'UA')
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValidationError('Invalid Phone Number')
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValidationError('Invalid phone number')

    def get_prep_value(self, value):

        if value:
            parsed_number = phonenumbers.parse(value, 'UA')
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        return value
