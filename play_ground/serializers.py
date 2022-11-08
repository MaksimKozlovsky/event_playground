from rest_framework import serializers
from .models import Event, Ticket, Company, CustomUser


class EventSerializer(serializers.ModelSerializer):
#    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
#        read_only_field = ['id']

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


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    tier_human = serializers.CharField(read_only=True, source='get_tier_display')

    class Meta:
        model = CustomUser
        fields = ["id", "username", "tier", "tier_human", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, instance: CustomUser, validated_data):
        if validated_data.get("password"):
            instance.set_password(validated_data.pop("password"))
        return super().update(instance, validated_data)

