from rest_framework import serializers

from main.models import Payments
from main.validators import CardNumberValidator, ExpirationDateValidator, CVCValidator


class PaymentsSerializer(serializers.ModelSerializer):
    card_number = serializers.CharField(validators=[CardNumberValidator('card_number')])
    expiration_date = serializers.CharField(validators=[ExpirationDateValidator('expiration_date')])
    cvc = serializers.CharField(validators=[CVCValidator('cvc')])

    class Meta:
        model = Payments
        fields = '__all__'
