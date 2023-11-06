import stripe
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Payments
from main.serializers.payments import PaymentsSerializer


class PaymentsListAPIView(ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ['date']


class PaymentStatusView(APIView):

    def get(self, request):
        payment_id = request.query_params.get('payment_id')

        try:
            payment = stripe.PaymentIntent.retrieve(payment_id)

            response_data = {
                'status': payment.status,
                'amount': payment.amount,
                'currency': payment.currency,
                'transfer_data': payment.transfer_data
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
