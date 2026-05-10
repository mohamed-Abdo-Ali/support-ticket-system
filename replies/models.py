from django.db import models
from django.contrib.auth.models import User
from tickets.models import Ticket

class Reply(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='replies') 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    message = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Reply by {self.user.username} on {self.ticket.subject}"