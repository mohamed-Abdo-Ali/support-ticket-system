from rest_framework import serializers
from .models import Reply

class ReplySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_fullname = serializers.CharField(source='user.first_name', read_only=True)
    is_staff = serializers.BooleanField(source='user.is_staff', read_only=True)

    class Meta:
        model = Reply
        fields = ['id', 'ticket', 'user', 'user_name', 'user_fullname', 'is_staff', 'message', 'created_at']
        read_only_fields = ['user', 'created_at']