from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tickets.models import Ticket
from .models import Reply

@login_required
def add_reply(request, ticket_pk):
    ticket = get_object_or_404(Ticket, pk=ticket_pk)
    
    # Only staff (non-superusers) can reply to tickets
    if not request.user.is_staff or request.user.is_superuser:
        messages.error(request, 'Only support staff (not managers) can reply to tickets.')
        return redirect('ticket_detail', pk=ticket_pk)
    
    if request.method == "POST":
        message = request.POST.get('message')
        
        if ticket.status == 'Closed':
            messages.error(request, 'Cannot reply to a closed ticket.')
        elif not message or message.strip() == "":
            messages.error(request, 'Reply cannot be empty.')
        else:
            Reply.objects.create(
                ticket=ticket,
                user=request.user,
                message=message
            )
            messages.success(request, 'Reply added successfully.')
            
            # Email Notification to Ticket Creator (simulated)
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                send_mail(
                    f'New Reply on Ticket #{ticket.id}',
                    f'Hello,\n\nA support member has replied to your ticket: "{ticket.subject}".\n\nReply: {message}',
                    settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@support.com',
                    [ticket.created_by.email],
                    fail_silently=True,
                )
            except:
                pass
            
    return redirect('ticket_detail', pk=ticket_pk)

@login_required
def edit_reply(request, pk):
    # Reply editing is strictly disabled for all users
    messages.error(request, 'Replies cannot be edited once posted for security and integrity.')
    reply = get_object_or_404(Reply, pk=pk)
    return redirect('ticket_detail', pk=reply.ticket.pk)

@login_required
def delete_reply(request, pk):
    # Reply deletion is strictly disabled for all users
    messages.error(request, 'Replies cannot be deleted once posted to maintain audit trail.')
    reply = get_object_or_404(Reply, pk=pk)
    return redirect('ticket_detail', pk=reply.ticket.pk)
