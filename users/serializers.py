from rest_framework import serializers

from main.serializers.payments import PaymentsSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentsSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'payments']
