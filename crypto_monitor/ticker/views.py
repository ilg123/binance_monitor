from rest_framework import generics
from .models import Ticker
from .serializers import TickerSerializer
from django_filters.rest_framework import DjangoFilterBackend

class TickerList(generics.ListAPIView):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['symbol', 'timestamp']