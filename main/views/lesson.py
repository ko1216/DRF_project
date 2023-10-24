from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from main.models import Lesson
from main.permissions import IsModerator, IsCourseOrLessonOwner, IsNotModerator
from main.serializers.lesson import LessonSerializer
from users.models import UserRoles


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsCourseOrLessonOwner, IsAuthenticated]


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.role == UserRoles.moderator:
                return Lesson.objects.all()
            return Lesson.objects.filter(payments__user=self.request.user).distinct()
        return Lesson.objects.none()


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
