import re

from rest_framework import serializers


class VideoLinkValidator:

    def __init__(self, field):
        self.field = field
        self.start_with = 'https://www.youtube.com/'

    def __call__(self, value):
        if not str(value).startswith(self.start_with):
            raise serializers.ValidationError('The video link must begin with https://www.youtube.com')


class CardNumberValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if len(value) != 16 and not value.isnumeric():
            raise serializers.ValidationError('The card number must be 16 digits')


class ExpirationDateValidator:

    def __init__(self, field):
        self.field = field
        self.date_format = re.compile(r'^\d{2}/\d{4}$')

    def __call__(self, value):
        if not self.date_format.match(value):
            raise serializers.ValidationError('The format of the expiration date must be "MM/YYYY"')


class CVCValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if len(value) != 3 and not value.isnumeric():
            raise serializers.ValidationError('The CVC number must be 3 digits')
