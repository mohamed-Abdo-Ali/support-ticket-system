from .models import Ticket
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404 
from replies.models import Reply
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Capture full name during registration
            fullname = request.POST.get('fullname')
            if fullname:
                user.first_name = fullname
                user.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_staff:
        base_qs = Ticket.objects.all()
    else:
        base_qs = Ticket.objects.filter(created_by=request.user)
        
    # Chart Data
    category_data = base_qs.values('category').annotate(count=Count('id'))
    status_data = base_qs.values('status').annotate(count=Count('id'))
        
    context = {
        'total_tickets': base_qs.count(), 
        'open_tickets': base_qs.filter(status='Open').count(), 
        'resolved_tickets': base_qs.filter(status='Resolved').count(), 
        'high_priority_tickets': base_qs.filter(priority='High').count(), 
        'category_labels': [item['category'] for item in category_data],
        'category_counts': [item['count'] for item in category_data],
        'status_labels': [item['status'] for item in status_data],
        'status_counts': [item['count'] for item in status_data],
    }
    return render(request, 'tickets/dashboard.html', context)

@login_required
@login_required
def ticket_list(request):
    if request.user.is_staff:
        tickets_list = Ticket.objects.all().order_by('-created_at')
    else:
        tickets_list = Ticket.objects.filter(created_by=request.user).order_by('-created_at')
    
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
    # Only regular users (non-staff) can create tickets
    if request.user.is_staff:
        messages.error(request, 'Support staff and managers cannot create tickets.')
        return redirect('dashboard')
    if request.method == "POST":
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        category = request.POST.get('category')
        
        attachment = request.FILES.get('attachment')
        
        if not subject or len(subject) < 5:
            messages.error(request, 'Subject must be at least 5 characters.')
            return render(request, 'tickets/ticket_form.html')

        ticket = Ticket.objects.create(
            subject=subject,
            description=description,
            priority=priority,
            category=category,
            created_by=request.user,
            attachment=attachment
        )
        messages.success(request, 'Ticket created successfully.')
        
        # Email Notification (simulated)
        try:
            send_mail(
                f'New Ticket: {subject}',
                f'A new ticket has been opened by {request.user.username}.\n\nDescription: {description}',
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@support.com',
                ['staff@support.com'], # In real world, send to all staff
                fail_silently=True,
            )
        except:
            pass

        return redirect('ticket_list')
    return render(request, 'tickets/ticket_form.html')

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    
    # Permission check: Creator or Staff only
    if ticket.created_by != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to view this ticket.')
        return redirect('ticket_list')
        
    replies_list = ticket.replies.all().order_by('created_at')
    # Pagination for replies (Bonus E)
    paginator = Paginator(replies_list, 5) # 5 replies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket, 'page_obj': page_obj})


@login_required
def edit_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    
    # Permissions: Only staff/admin can edit
    if not request.user.is_staff:
        messages.error(request, 'Only support staff can edit tickets.')
        return redirect('ticket_detail', pk=pk)
    
    # Closed tickets cannot be edited by ANYONE (even staff)
    if ticket.status == 'Closed':
        messages.error(request, 'This ticket is closed and cannot be edited by anyone.')
        return redirect('ticket_detail', pk=pk)

    
    if request.method == "POST":
        # If user is staff, they can ONLY update the status
        if request.user.is_staff:
            new_status = request.POST.get('status')
            if new_status:
                ticket.status = new_status
                ticket.save()
                messages.success(request, f'Ticket status updated to {new_status}.')
            return redirect('ticket_detail', pk=ticket.pk)
            
        # For non-staff (though currently blocked by permissions above, keeping logic for safety)
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
    
    # Permissions: Only staff/admin can delete
    if not request.user.is_staff:
        messages.error(request, 'Only support staff can delete tickets.')
        return redirect('ticket_list')
        
    # Tickets can ONLY be deleted if they are Closed
    if ticket.status != 'Closed':
        messages.error(request, 'Tickets must be Closed before they can be deleted.')
        return redirect('ticket_detail', pk=pk)
        
    ticket.delete()
    messages.success(request, 'Ticket deleted successfully.')
    return redirect('ticket_list')

@login_required
def user_list(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Only managers can manage users.')
        return redirect('dashboard')
    
    users = User.objects.annotate(
        ticket_count=Count('tickets'),
    ).order_by('-date_joined')
    
    return render(request, 'tickets/user_list.html', {'users': users})

@login_required
def user_create(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Only managers can manage users.')
        return redirect('dashboard')
    
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_staff = request.POST.get('is_staff') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'
        
        if not username or not password:
            messages.error(request, 'Username and password are required.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.first_name = request.POST.get('fullname', '') # Store full name
            user.save()
            messages.success(request, f'User {username} created successfully.')
            return redirect('user_list')
            
    return render(request, 'tickets/user_form.html')

@login_required
def user_edit(request, pk):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Only managers can manage users.')
        return redirect('dashboard')
        
    target_user = get_object_or_404(User, pk=pk)
    
    if request.method == "POST":
        username = request.POST.get('username')
        if not username:
            messages.error(request, 'Username is required.')
            return render(request, 'tickets/user_form.html', {'target_user': target_user})

        target_user.username = username
        target_user.email = request.POST.get('email')
        target_user.first_name = request.POST.get('fullname', '') # Update full name
        
        if request.user.is_superuser:
            target_user.is_staff = request.POST.get('is_staff') == 'on'
            target_user.is_superuser = request.POST.get('is_superuser') == 'on'
        
        new_password = request.POST.get('password')
        if new_password:
            target_user.set_password(new_password)
            
        target_user.save()
        messages.success(request, f'User {target_user.username} updated.')
        return redirect('user_list')
        
    return render(request, 'tickets/user_form.html', {'target_user': target_user})

@login_required
def user_delete(request, pk):
    if not request.user.is_superuser:
        messages.error(request, 'Only superusers can delete users.')
        return redirect('user_list')
        
    target_user = get_object_or_404(User, pk=pk)
    if target_user == request.user:
        messages.error(request, 'You cannot delete yourself.')
    else:
        target_user.delete()
        messages.success(request, 'User deleted successfully.')
        
    return redirect('user_list')

@login_required
def user_detail(request, pk):
    if not request.user.is_staff and request.user.pk != pk:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
        
    viewed_user = get_object_or_404(User, pk=pk)
    user_tickets = viewed_user.tickets.all().order_by('-created_at')
    
    return render(request, 'tickets/user_detail.html', {
        'viewed_user': viewed_user,
        'user_tickets': user_tickets
    })

@login_required
def profile(request):
    if request.method == "POST":
        request.user.first_name = request.POST.get('fullname')
        request.user.email = request.POST.get('email')
        request.user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    return render(request, 'tickets/profile.html')


