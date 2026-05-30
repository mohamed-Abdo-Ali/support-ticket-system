from rest_framework import serializers
from tickets.models import Ticket  # تأكد من استيراد الموديل بشكل صحيح

class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket  
        fields = "__all__"