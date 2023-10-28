from rest_framework import serializers

from main.models import Course
from main.serializers.lesson import LessonSerializer, LessonSerializerForCourse


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializerForCourse(many=True, read_only=True)
    is_subscribed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Course
        fields = ['title', 'description', 'lessons_count', 'lessons', 'is_subscribed']

    def get_lessons_count(self, instance):
        if instance.lessons.all():
            return len(instance.lessons.all())
        else:
            return 0
