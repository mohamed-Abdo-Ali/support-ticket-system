from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tickets.models import Ticket
from .models import Reply

@login_required
def add_reply(request, ticket_pk):
    ticket = get_object_or_404(Ticket, pk=ticket_pk)
    
    # Only staff can reply to tickets
    if not request.user.is_staff:
        messages.error(request, 'Only support staff can reply to tickets.')
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
            
    return redirect('ticket_detail', pk=ticket_pk)

@login_required
def edit_reply(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    
    # Permissions: Only author or staff can edit
    if reply.user != request.user and not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('ticket_detail', pk=reply.ticket.pk)
        
    if request.method == "POST":
        message = request.POST.get('message')
        if not message or message.strip() == "":
            messages.error(request, 'Reply cannot be empty.')
        else:
            reply.message = message
            reply.save()
            messages.success(request, 'Reply updated.')
            return redirect('ticket_detail', pk=reply.ticket.pk)
            
    return render(request, 'replies/reply_edit.html', {'reply': reply})

@login_required
def delete_reply(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    ticket_pk = reply.ticket.pk
    
    # Permissions: Only author or staff can delete
    if reply.user != request.user and not request.user.is_staff:
        messages.error(request, 'Access denied.')
    else:
        reply.delete()
        messages.success(request, 'Reply deleted.')
        
    return redirect('ticket_detail', pk=ticket_pk)
