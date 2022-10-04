from rest_framework import serializers
from .models import Event, Ticket, Company


class EventSerializer(serializers.ModelSerializer):
#    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'date', 'title')
        read_only_field = ['id']

    def create(self, validated_data):
        validated_data['ticket_count'] = validated_data.get('ticket_count', 20)
        return super().create(validated_data)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('price', 'number', 'vip', 'id')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('title',)
