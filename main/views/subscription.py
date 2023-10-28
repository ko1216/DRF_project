from rest_framework.generics import CreateAPIView, DestroyAPIView

from main.models import Subscription
from main.serializers.subscription import SubscriptionSerializer


class SubscriptionCreateAPIView(CreateAPIView):
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        """
        За основуную логику создания подписки отвечает сериалайзер. В этом методе мы меняем ддефолтное значение подписки
        на True
        """
        serializer.save(is_active=True)


class SubscriptionDestroyAPIView(DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
