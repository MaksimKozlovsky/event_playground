from rest_framework import serializers
from .models import Event, Ticket, Company


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'date', 'title', 'description')
