from django.urls import path
from rest_framework.routers import DefaultRouter

from main.views.lesson import LessonListAPIView, LessonRetrieveAPIView, LessonCreateAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView
from main.views.course import CourseViewSet, CoursePayView

from main.apps import MainConfig
from main.views.payments import PaymentsListAPIView
from main.views.subscription import SubscriptionCreateAPIView, SubscriptionDestroyAPIView

app_name = MainConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')


urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lessons_list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_detail'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
    path('payments/', PaymentsListAPIView.as_view(), name='payments_list'),
    path('subscription/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('subscription/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='subscription_delete'),
    path('course/pay/<int:course_id>/', CoursePayView.as_view(), name='course_pay'),
] + router.urls
