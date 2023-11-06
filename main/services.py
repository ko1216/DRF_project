import stripe
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment_intent(price: int, currency: str = 'rub'):
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=price,
            currency=currency,
            description='Оплата курса',
            payment_method_types=['card'],
        )
        return str(payment_intent.id)
    except stripe.error.StripeError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def get_payment_intent_status(payment_intent_id):
    try:
        payment = stripe.PaymentIntent.retrieve(payment_intent_id)

        response = {
            'status': payment.status,
            'amount': payment.amount,
            'currency': payment.currency,
            'transfer_data': payment.transfer_data
        }

        return Response(response, status=status.HTTP_200_OK)
    except stripe.error.StripeError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
