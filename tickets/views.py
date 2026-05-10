from .models import Ticket
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404 
from replies.models import Reply
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.db.models import Q

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    context = {
        'total_tickets': Ticket.objects.count(), 
        'open_tickets': Ticket.objects.filter(status='Open').count(), 
        'resolved_tickets': Ticket.objects.filter(status='Resolved').count(), 
        'high_priority_tickets': Ticket.objects.filter(priority='High').count(), 
    }
    return render(request, 'tickets/dashboard.html', context)

@login_required
def ticket_list(request):
    tickets_list = Ticket.objects.all().order_by('-created_at')
    
    # Search & Filters (Bonus B)
    query = request.GET.get('q')
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    
    if query:
        tickets_list = tickets_list.filter(Q(subject__icontains=query) | Q(description__icontains=query))
    if status_filter:
        tickets_list = tickets_list.filter(status=status_filter)
    if priority_filter:
        tickets_list = tickets_list.filter(priority=priority_filter)
        
    # Pagination (Bonus E)
    paginator = Paginator(tickets_list, 10) # 10 tickets per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'tickets/ticket_list.html', {
        'page_obj': page_obj,
        'query': query,
        'status_filter': status_filter,
        'priority_filter': priority_filter
    })

@login_required
def create_ticket(request):
    if request.method == "POST":
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        category = request.POST.get('category')
        
        if not subject or len(subject) < 5:
            messages.error(request, 'Subject must be at least 5 characters.')
            return render(request, 'tickets/ticket_form.html')

        ticket = Ticket.objects.create(
            subject=subject,
            description=description,
            priority=priority,
            category=category,
            created_by=request.user
        )
        messages.success(request, 'Ticket created successfully.')
        return redirect('ticket_list')
    return render(request, 'tickets/ticket_form.html')

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    replies_list = ticket.replies.all().order_by('created_at')

    # Pagination for replies (Bonus E)
    paginator = Paginator(replies_list, 5) # 5 replies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        message = request.POST.get('message')
        
        if ticket.status == 'Closed':
            messages.error(request, 'Cannot reply to a closed ticket.')
            return redirect('ticket_detail', pk=pk)
        
        if not message or message.strip() == "":
            messages.error(request, 'Reply cannot be empty.')
            return redirect('ticket_detail', pk=pk)

        Reply.objects.create(
            ticket=ticket,
            user=request.user,
            message=message
        )
        messages.success(request, 'Reply added successfully.')
        return redirect('ticket_detail', pk=pk)

    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket, 'page_obj': page_obj})

@login_required
def edit_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    
    # Permissions: Only creator or admin can edit (Bonus C)
    if ticket.created_by != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this ticket.')
        return redirect('ticket_detail', pk=pk)
    
    if request.method == "POST":
        subject = request.POST.get('subject')
        if not subject or len(subject) < 5:
            messages.error(request, 'Subject must be at least 5 characters.')
            return render(request, 'tickets/ticket_form.html', {'ticket': ticket})
            
        ticket.subject = subject
        ticket.description = request.POST.get('description')
        ticket.priority = request.POST.get('priority')
        ticket.category = request.POST.get('category')
        ticket.status = request.POST.get('status')
        ticket.save()
        
        messages.success(request, 'Ticket updated successfully.')
        return redirect('ticket_detail', pk=ticket.pk)
    
    return render(request, 'tickets/ticket_form.html', {'ticket': ticket})

@login_required
def delete_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    
    # Permissions: Only creator or admin can delete (Bonus C)
    if ticket.created_by != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this ticket.')
        return redirect('ticket_list')
        
    ticket.delete()
    messages.success(request, 'Ticket deleted successfully.')
    return redirect('ticket_list')