from rest_framework.viewsets import ModelViewSet

from main.models import Course
from main.serializers.course import CourseSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
