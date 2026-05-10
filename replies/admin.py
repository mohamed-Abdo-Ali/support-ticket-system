from django.contrib import admin
from .models import Reply

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('message',)
