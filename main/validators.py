from rest_framework import serializers


class VideoLinkValidator:

    def __init__(self, field):
        self.field = field
        self.start_with = 'https://www.youtube.com/'

    def __call__(self, value):
        if not str(value).startswith(self.start_with):
            raise serializers.ValidationError('The video link must begin with https://www.youtube.com')
