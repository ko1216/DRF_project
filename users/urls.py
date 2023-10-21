from django.urls import path

from users.apps import UsersConfig
from users.views import UserListAPIView, UserRetrieveAPIView

app_name = UsersConfig.name


urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='users_list'),
    path('user/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_retrieve'),
]
