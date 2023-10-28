from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from main.models import Course, Subscription
from main.pagination import SubjectsPagination
from main.permissions import IsModerator, IsCourseOrLessonOwner, IsNotModerator
from main.serializers.course import CourseSerializer
from users.models import UserRoles


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = SubjectsPagination

    def get_permissions(self):
        # Определяем разрешения в зависимости от действия
        if self.action in ['list']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['retrieve']:
            permission_classes = [IsCourseOrLessonOwner]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsModerator | IsCourseOrLessonOwner]
        elif self.action in ['destroy']:
            permission_classes = [IsCourseOrLessonOwner]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.role == UserRoles.moderator:
                return Course.objects.all()
            return Course.objects.filter(payments__user=self.request.user)
        return Course.objects.none()

    def list(self, request, *args, **kwargs):
        user = request.user
        courses = Course.objects.all()

        for course in courses:
            is_subscribed = Subscription.objects.filter(user=user, course=course).exists()
            course.is_subscribed = is_subscribed

        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        queryset = Course.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = CourseSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)
