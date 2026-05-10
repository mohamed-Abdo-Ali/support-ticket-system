from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Ticket
from replies.models import Reply

class SupportTicketTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.other_user = User.objects.create_user(username='otheruser', password='password123')
        self.admin_user = User.objects.create_superuser(username='admin', password='password123', email='admin@test.com')
        
    def test_dashboard_login_required(self):
        # Dashboard should redirect to login if not authenticated
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        
    def test_ticket_creation_logic(self):
        self.client.login(username='testuser', password='password123')
        
        # Valid ticket
        response = self.client.post(reverse('create_ticket'), {
            'subject': 'Valid Subject',
            'description': 'Valid Description',
            'priority': 'Medium',
            'category': 'General'
        })
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(response.status_code, 302) # Redirect to list
        
        # Invalid ticket (short subject)
        response = self.client.post(reverse('create_ticket'), {
            'subject': 'ABC',
            'description': 'Valid Description',
            'priority': 'Medium',
            'category': 'General'
        })
        # It should stay on form and show error (or at least not create ticket)
        self.assertEqual(Ticket.objects.count(), 1) 
        
    def test_reply_on_closed_ticket(self):
        self.client.login(username='testuser', password='password123')
        ticket = Ticket.objects.create(
            subject='Closed Ticket',
            description='Test',
            status='Closed',
            created_by=self.user
        )
        
        response = self.client.post(reverse('ticket_detail', args=[ticket.pk]), {
            'message': 'This should fail'
        })
        
        # Reply count should be 0
        self.assertEqual(Reply.objects.count(), 0)
        
    def test_permissions_edit_delete(self):
        # User A creates a ticket
        ticket = Ticket.objects.create(
            subject='User A Ticket',
            description='Test',
            created_by=self.user
        )
        
        # User B tries to edit
        self.client.login(username='otheruser', password='password123')
        response = self.client.post(reverse('edit_ticket', args=[ticket.pk]), {
            'subject': 'Modified Subject',
            'status': 'Resolved'
        })
        ticket.refresh_from_db()
        self.assertNotEqual(ticket.subject, 'Modified Subject')
        
        # Admin tries to edit
        self.client.login(username='admin', password='password123')
        response = self.client.post(reverse('edit_ticket', args=[ticket.pk]), {
            'subject': 'Admin Modified Subject',
            'description': 'Test',
            'priority': 'Medium',
            'category': 'General',
            'status': 'Resolved'
        })
        ticket.refresh_from_db()
        self.assertEqual(ticket.subject, 'Admin Modified Subject')
        self.assertEqual(ticket.status, 'Resolved')

