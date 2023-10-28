from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Course, Lesson, Payments
from users.models import User, UserRoles


class LessonRetrieveTestCase(APITestCase):

    def setUp(self) -> None:
        self.course = Course.objects.create(
            title='Тестовый курс 1',
            description='Описание для тестового курса'
        )

        self.lesson_1 = Lesson.objects.create(
            title='Тестовый урок 1.0',
            description='Описание для тестового урока 1.0',
            video_link='https://www.youtube.com/watch',
            course=self.course
        )

        self.member_user = User.objects.create(
            email='member@example.com',
            password='123qwe456rty',
        )

        self.member_user_2 = User.objects.create(
            email='member2@example.com',
            password='123qwe456rty',
        )

        self.payment_for_1 = Payments.objects.create(
            user=self.member_user,
            lesson=self.lesson_1,
            amount=2000,
            payment_method='наличными'
        )

    def test_get(self):
        """
        Test for getting detail lesson's information
        """
        self.client.force_authenticate(user=self.member_user)

        response = self.client.get(reverse('main:lesson_detail', kwargs={'pk': self.lesson_1.pk}))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": self.lesson_1.id,
                "video_link": self.lesson_1.video_link,
                "title": self.lesson_1.title,
                "description": self.lesson_1.description,
                "preview": None,
                "course": self.lesson_1.course_id
            }
        )

    def test_not_owner(self):
        self.client.force_authenticate(user=self.member_user_2)

        response = self.client.get(reverse('main:lesson_detail', kwargs={'pk': self.lesson_1.pk}))

        self.assertEqual(
            response.json(),
            {
                "detail": "Вы не являетесь владельцем"
            }
        )

    def test_not_authenticated(self):
        response = self.client.get(reverse('main:lesson_detail', kwargs={'pk': self.lesson_1.pk}))

        self.assertEqual(
            response.json(),
            {
                'detail': 'Authentication credentials were not provided.'
            }
        )


class LessonListTestCase(APITestCase):

    def setUp(self) -> None:
        self.course = Course.objects.create(
            title='Тестовый курс 1',
            description='Описание для тестового курса'
        )

        self.lesson_1 = Lesson.objects.create(
            title='Тестовый урок 1.0',
            description='Описание для тестового урока 1.0',
            video_link='https://www.youtube.com/watch',
            course=self.course
        )

        self.member_user = User.objects.create(
            email='member@example.com',
            password='123qwe456rty',
        )

        self.moderator_user = User.objects.create(
            email='admin@example.com',
            password='123qwe456rty',
            role=UserRoles.moderator
        )

        self.member_user_2 = User.objects.create(
            email='member2@example.com',
            password='123qwe456rty',
        )

        self.payment_for_1 = Payments.objects.create(
            user=self.member_user,
            lesson=self.lesson_1,
            amount=2000,
            payment_method='наличными'
        )

    def test_get(self):
        """
        Test for getting list of lessons
        """
        self.client.force_authenticate(user=self.member_user)

        response = self.client.get(reverse('main:lessons_list'))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson_1.id,
                        "video_link": self.lesson_1.video_link,
                        "title": self.lesson_1.title,
                        "description": self.lesson_1.description,
                        "preview": None,
                        "course": self.lesson_1.course_id
                    }
                ]
            }
        )

    def test_not_owner(self):
        self.client.force_authenticate(user=self.member_user_2)

        response = self.client.get(reverse('main:lessons_list'))

        self.assertEqual(
            response.json(),
            {
                "count": 0,
                "next": None,
                "previous": None,
                "results": [

                ]
            }
        )

    def test_non_authenticated(self):
        response = self.client.get(reverse('main:lessons_list'))

        self.assertEqual(
            response.json(),
            {
                "detail": "Authentication credentials were not provided."
            }
        )

    def test_moderators_root(self):
        self.client.force_authenticate(user=self.moderator_user)

        response = self.client.get(reverse('main:lessons_list'))

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson_1.id,
                        "video_link": self.lesson_1.video_link,
                        "title": self.lesson_1.title,
                        "description": self.lesson_1.description,
                        "preview": None,
                        "course": self.lesson_1.course_id
                    }
                ]
            }
        )


class LessonCreateTestCase(APITestCase):

    def setUp(self):
        self.course = Course.objects.create(
            title='Тестовый курс 1',
            description='Описание для тестового курса'
        )

        self.member_user = User.objects.create(
            email='member@example.com',
            password='123qwe456rty',
        )

        self.moderator_user = User.objects.create(
            email='admin@example.com',
            password='123qwe456rty',
            role=UserRoles.moderator
        )

        self.new_lesson = {
            'title': 'Тестовый урок 1.0',
            'description': 'Описание для тестового урока 1.0',
            'video_link': 'https://www.youtube.com/watch',
            'course': self.course.id
        }

        self.new_lesson_valid_error = {
            'title': 'Тестовый урок 1.0',
            'description': 'Описание для тестового урока 1.0',
            'video_link': 'https://www.other_host.com/watch',
            'course': self.course.id
        }

    def test_create_if_moderator(self):
        self.client.force_authenticate(user=self.moderator_user)

        response = self.client.post(
            reverse('main:lesson_create'),
            self.new_lesson
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(
            response.json(),
            {
                "detail": "You do not have permission to perform this action."
            }
        )

    def test_create(self):
        self.client.force_authenticate(user=self.member_user)

        response = self.client.post(
            reverse('main:lesson_create'),
            self.new_lesson
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {
                "id": 1,
                "video_link": 'https://www.youtube.com/watch',
                "title": 'Тестовый урок 1.0',
                "description": 'Описание для тестового урока 1.0',
                "preview": None,
                "course": 1
            }
        )

    def test_create_non_authenticated(self):
        response = self.client.post(
            reverse('main:lesson_create'),
            self.new_lesson
        )

        self.assertEqual(
            response.json(),
            {
                "detail": "Authentication credentials were not provided."
            }
        )

    def test_create_validation_errors(self):
        self.client.force_authenticate(user=self.member_user)

        response = self.client.post(
            reverse('main:lesson_create'),
            self.new_lesson_valid_error
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                'video_link':
                    ['The video link must begin with https://www.youtube.com',
                     'Enter a valid URL.']

            }
        )


class LessonUpdateTestCase(APITestCase):
    def setUp(self) -> None:
        self.course = Course.objects.create(
            title='Тестовый курс 1',
            description='Описание для тестового курса'
        )

        self.lesson_1 = Lesson.objects.create(
            title='Тестовый урок 1.0',
            description='Описание для тестового урока 1.0',
            video_link='https://www.youtube.com/watch',
            course=self.course
        )

        self.member_user = User.objects.create(
            email='member@example.com',
            password='123qwe456rty',
        )

        self.moderator_user = User.objects.create(
            email='admin@example.com',
            password='123qwe456rty',
            role=UserRoles.moderator
        )

        self.member_user_2 = User.objects.create(
            email='member2@example.com',
            password='123qwe456rty',
        )

        self.payment_for_1 = Payments.objects.create(
            user=self.member_user,
            lesson=self.lesson_1,
            amount=2000,
            payment_method='наличными'
        )

    def test_update_by_owner(self):
        self.client.force_authenticate(user=self.member_user)

        response = self.client.patch(reverse('main:lesson_update', kwargs={'pk': self.lesson_1.pk}),
                                     {"description": "Новое описание"})

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": self.lesson_1.id,
                "video_link": self.lesson_1.video_link,
                "title": self.lesson_1.title,
                "description": "Новое описание",
                "preview": None,
                "course": self.lesson_1.course_id
            }
        )

    def test_update_by_moderator(self):
        self.client.force_authenticate(user=self.moderator_user)

        response = self.client.patch(reverse('main:lesson_update', kwargs={'pk': self.lesson_1.pk}),
                                     {"description": "Новое описание"})

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": self.lesson_1.id,
                "video_link": self.lesson_1.video_link,
                "title": self.lesson_1.title,
                "description": "Новое описание",
                "preview": None,
                "course": self.lesson_1.course_id
            }
        )

    def test_update_by_non_owner(self):
        self.client.force_authenticate(user=self.member_user_2)

        response = self.client.patch(reverse('main:lesson_update', kwargs={'pk': self.lesson_1.pk}),
                                     {"description": "Новое описание"})

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(
            response.json(),
            {
                "detail": "You do not have permission to perform this action."
            }
        )

    def test_update_by_non_authorized(self):
        response = self.client.patch(reverse('main:lesson_update', kwargs={'pk': self.lesson_1.pk}),
                                     {"description": "Новое описание"})

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.assertEqual(
            response.json(),
            {
                "detail": "Authentication credentials were not provided."
            }
        )


class LessonDestroyTestCase(APITestCase):
    def setUp(self) -> None:
        self.course = Course.objects.create(
            title='Тестовый курс 1',
            description='Описание для тестового курса'
        )

        self.lesson_1 = Lesson.objects.create(
            title='Тестовый урок 1.0',
            description='Описание для тестового урока 1.0',
            video_link='https://www.youtube.com/watch',
            course=self.course
        )

        self.member_user = User.objects.create(
            email='member@example.com',
            password='123qwe456rty',
        )

        self.moderator_user = User.objects.create(
            email='admin@example.com',
            password='123qwe456rty',
            role=UserRoles.moderator
        )

        self.member_user_2 = User.objects.create(
            email='member2@example.com',
            password='123qwe456rty',
        )

        self.payment_for_1 = Payments.objects.create(
            user=self.member_user,
            lesson=self.lesson_1,
            amount=2000,
            payment_method='наличными'
        )

    def test_destroy_by_owner(self):
        self.client.force_authenticate(user=self.member_user)

        response = self.client.delete(reverse('main:lesson_delete', kwargs={'pk': self.lesson_1.pk}))

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_destroy_by_moderator(self):
        self.client.force_authenticate(user=self.moderator_user)

        response = self.client.delete(reverse('main:lesson_delete', kwargs={'pk': self.lesson_1.pk}))

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(
            response.json(),
            {
                "detail": "Вы не являетесь владельцем"
            }
        )

    def test_destroy_by_non_owner(self):
        self.client.force_authenticate(user=self.member_user_2)

        response = self.client.delete(reverse('main:lesson_delete', kwargs={'pk': self.lesson_1.pk}))

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(
            response.json(),
            {
                "detail": "Вы не являетесь владельцем"
            }
        )

    def test_destroy_by_non_authorized(self):
        response = self.client.delete(reverse('main:lesson_delete', kwargs={'pk': self.lesson_1.pk}))

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.assertEqual(
            response.json(),
            {
                "detail": "Authentication credentials were not provided."
            }
        )
