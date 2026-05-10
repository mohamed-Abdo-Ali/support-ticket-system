from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Ticket(models.Model):
    # خيارات الحالة [cite: 68]
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]
    
    # خيارات الأولوية [cite: 75]
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    
    # خيارات التصنيف [cite: 80]
    CATEGORY_CHOICES = [
        ('Technical', 'Technical'),
        ('Billing', 'Billing'),
        ('General', 'General'),
    ]

    subject = models.CharField(max_length=255) # 
    description = models.TextField() # 
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium') # 
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='General') # 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open') # 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets') # [cite: 53, 102]
    created_at = models.DateTimeField(auto_now_add=True) # 

    def __str__(self):
        return self.subject