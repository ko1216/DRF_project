from rest_framework import serializers

from main.models import Course


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['title', 'description', 'lessons_count', 'lessons']

    def get_lessons_count(self, instance):
        if instance.lessons.all():
            return len(instance.lessons.all())
        else:
            return 0

    def get_lessons(self, instance):
        return [lesson.title for lesson in instance.lessons.all()]
