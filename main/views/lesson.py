from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from main.models import Lesson
from main.pagination import SubjectsPagination
from main.permissions import IsModerator, IsCourseOrLessonOwner, IsNotModerator
from main.serializers.lesson import LessonSerializer
from users.models import UserRoles


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsCourseOrLessonOwner, IsAuthenticated]


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = SubjectsPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Lesson.objects.all()
        ordering = self.request.query_params.get('ordering', 'id')

        if self.request.user.is_authenticated:
            if self.request.user.role == UserRoles.moderator:
                return queryset.order_by(ordering)
            return Lesson.objects.filter(payments__user=self.request.user).distinct()
        return Lesson.objects.none()

    def get(self, request, *args, **kwargs):
        ordering = self.request.query_params.get('ordering', 'id')
        queryset = self.get_queryset().order_by(ordering)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = LessonSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsCourseOrLessonOwner, IsAuthenticated]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsCourseOrLessonOwner, IsAuthenticated]
