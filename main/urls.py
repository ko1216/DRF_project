from django.urls import path
from rest_framework.routers import DefaultRouter

from main.views.lesson import *
from main.views.course import *

from main.apps import MainConfig

app_name = MainConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view()),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), ),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), ),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), ),
] + router.urls
