from rest_framework import serializers

from main.models import Lesson
from main.permissions import IsCourseOrLessonOwner
from main.validators import VideoLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.URLField(validators=[VideoLinkValidator('video_link')])

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonSerializerForCourse(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        permission_classes = [IsCourseOrLessonOwner]
