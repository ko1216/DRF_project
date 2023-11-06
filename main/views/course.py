from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from main.models import Course, Subscription, Payments
from main.pagination import SubjectsPagination
from main.permissions import IsModerator, IsCourseOrLessonOwner, IsNotModerator
from main.serializers.course import CourseSerializer
from users.models import UserRoles
from django.conf import settings

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


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
        user = self.request.user
        courses = Course.objects.all()

        for course in courses:
            is_subscribed = Subscription.objects.filter(user=user, course=course).exists()
            course.is_subscribed = is_subscribed

        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self):
        queryset = Course.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = CourseSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class CoursePayView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        user = self.request.user
        amount = course.price_rub

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'rub',
                            'product_data': {
                                'name': course.title,
                            },
                            'unit_amount': amount,
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url='https://example.com/success/',
                cancel_url='https://example.com/cancel/',
            )

            payment = Payments.objects.create(
                user=user,
                course=course,
                amount=amount,
            )
            payment.card_number = request.data.get('card_number')
            payment.expiration_date = request.data.get('expiration_date')
            payment.cvc = request.data.get('cvc')
            payment.save()

            return Response({'sessionID': session.id, 'stripeCheckoutURL': session.url})

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
