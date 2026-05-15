from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]
    
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    
    CATEGORY_CHOICES = [
        ('Technical', 'Technical'),
        ('Billing', 'Billing'),
        ('General', 'General'),
    ]

    subject = models.CharField(max_length=255) # 
    description = models.TextField() # 
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium') 
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='General')  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open') 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets') 
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.ImageField(upload_to='ticket_attachments/', null=True, blank=True)

    @property
    def is_late(self):
        from django.utils import timezone
        from datetime import timedelta
        return self.status == 'Open' and (timezone.now() - self.created_at) > timedelta(hours=24)

    def __str__(self):
        return self.subject