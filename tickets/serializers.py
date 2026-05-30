from django.contrib.auth.models import User
from rest_framework import serializers
from tickets.models import Ticket

class UserSerializer(serializers.ModelSerializer):
    ticket_count = serializers.IntegerField(read_only=True)
    fullname = serializers.CharField(source='first_name', required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'fullname', 'is_staff', 'is_superuser', 'date_joined', 'ticket_count', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class TicketsSerializer(serializers.ModelSerializer):
    created_by_details = UserSerializer(source='created_by', read_only=True)
    created_by_name = serializers.SerializerMethodField()
    is_late = serializers.BooleanField(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'subject', 'description', 'priority', 'category', 'status',
            'created_by', 'created_by_details', 'created_by_name', 'created_at', 'attachment', 'is_late'
        ]
        read_only_fields = ['created_by', 'created_at']

    def get_created_by_name(self, obj):
        if obj.created_by.first_name:
            return obj.created_by.first_name
        return obj.created_by.username