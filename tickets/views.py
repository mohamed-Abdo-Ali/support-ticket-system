import re
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers

from .models import Ticket
from .serializers import TicketsSerializer, UserSerializer

class IsCreatorOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow if user is staff or is the creator of the ticket
        return request.user.is_staff or obj.created_by == request.user

class TicketPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketsSerializer
    permission_classes = [permissions.IsAuthenticated, IsCreatorOrStaff]
    pagination_class = TicketPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Ticket.objects.all().order_by('-created_at')
            created_by = self.request.query_params.get('created_by')
            if created_by:
                queryset = queryset.filter(created_by_id=created_by)
        else:
            queryset = Ticket.objects.filter(created_by=user).order_by('-created_at')

        # Filters
        query = self.request.query_params.get('q')
        status_filter = self.request.query_params.get('status')
        priority_filter = self.request.query_params.get('priority')

        if query:
            from django.db.models import Q
            queryset = queryset.filter(Q(subject__icontains=query) | Q(description__icontains=query))
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)

        return queryset

    def perform_create(self, serializer):
        # Staff and superusers cannot create tickets
        if self.request.user.is_staff:
            raise serializers.ValidationError({"detail": "Support staff and managers cannot create tickets."})
        
        subject = self.request.data.get('subject')
        description = self.request.data.get('description')
        if not subject or len(subject) < 5:
            raise serializers.ValidationError({"subject": "Subject must be at least 5 characters."})
            
        ticket = serializer.save(created_by=self.request.user)
        
        # Email Notification (simulated)
        try:
            from django.core.mail import send_mail
            send_mail(
                f'New Ticket: {ticket.subject}',
                f'A new ticket has been opened by {self.request.user.username}.\n\nDescription: {ticket.description}',
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@support.com',
                ['staff@support.com'],
                fail_silently=True,
            )
        except:
            pass

    def update(self, request, *args, **kwargs):
        # Permissions: Only staff/admin can edit
        if not request.user.is_staff:
            return Response({"detail": "Only support staff can edit tickets."}, status=status.HTTP_403_FORBIDDEN)
        
        ticket = self.get_object()
        
        # Closed tickets cannot be edited by ANYONE
        if ticket.status == 'Closed':
            return Response({"detail": "This ticket is closed and cannot be edited by anyone."}, status=status.HTTP_400_BAD_REQUEST)
            
        # If user is staff, they can ONLY update the status
        if request.user.is_staff:
            new_status = request.data.get('status')
            if new_status:
                ticket.status = new_status
                ticket.save()
                return Response(self.get_serializer(ticket).data)
            return Response({"detail": "Status field is required for support staff update."}, status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Only staff/admin can delete
        if not request.user.is_staff:
            return Response({"detail": "Only support staff can delete tickets."}, status=status.HTTP_403_FORBIDDEN)
            
        ticket = self.get_object()
        # Tickets can ONLY be deleted if they are Closed
        if ticket.status != 'Closed':
            return Response({"detail": "Tickets must be Closed before they can be deleted."}, status=status.HTTP_400_BAD_REQUEST)
            
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUser]

    def get_queryset(self):
        return User.objects.annotate(ticket_count=Count('tickets')).order_by('-date_joined')

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        fullname = request.data.get('fullname')
        email = request.data.get('email')

        if not username or not password:
            return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
            
        if User.objects.filter(username=username).exists():
            return Response({"detail": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
            
        user = User.objects.create_user(username=username, email=email, password=password)
        if fullname:
            user.first_name = fullname
            user.save()
            
        return Response({"detail": "Registration successful. Please log in."}, status=status.HTTP_201_CREATED)

class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            base_qs = Ticket.objects.all()
        else:
            base_qs = Ticket.objects.filter(created_by=request.user)
            
        # Chart Data
        category_data = base_qs.values('category').annotate(count=Count('id'))
        status_data = base_qs.values('status').annotate(count=Count('id'))
            
        data = {
            'total_tickets': base_qs.count(), 
            'open_tickets': base_qs.filter(status='Open').count(), 
            'resolved_tickets': base_qs.filter(status='Resolved').count(), 
            'high_priority_tickets': base_qs.filter(priority='High').count(), 
            'Low_priority_tickets': base_qs.filter(priority='Low').count(), 
            'Medium_priority_tickets': base_qs.filter(priority='Medium').count(), 
            'closed_tickets': base_qs.filter(status='Closed').count(),
            'in_progress_tickets': base_qs.filter(status='In Progress').count(),

            'category_labels': [item['category'] for item in category_data],
            'category_counts': [item['count'] for item in category_data],
            'status_labels': [item['status'] for item in status_data],
            'status_counts': [item['count'] for item in status_data],

        }
        return Response(data)

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        fullname = request.data.get('fullname')
        email = request.data.get('email')
        password = request.data.get('password')

        if fullname is not None:
            user.first_name = fullname
        if email is not None:
            user.email = email
        if password:
            user.set_password(password)
        user.save()
        
        serializer = UserSerializer(user)
        return Response(serializer.data)

class TranslationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, lang):
        if lang not in ['ar', 'en']:
            return Response({"detail": "Language not supported"}, status=status.HTTP_400_BAD_REQUEST)
            
        if lang == 'en':
            return Response({})
            
        po_path = settings.BASE_DIR / 'locale' / lang / 'LC_MESSAGES' / 'django.po'
        translations = {}
        if po_path.exists():
            try:
                with open(po_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                lines = content.split('\n')
                current_msgid = None
                current_msgstr = None
                in_msgid = False
                in_msgstr = False
                
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    if line.startswith('msgid '):
                        if current_msgid and current_msgstr:
                            translations[current_msgid] = current_msgstr
                        current_msgid = line[6:].strip('"')
                        current_msgstr = ""
                        in_msgid = True
                        in_msgstr = False
                    elif line.startswith('msgstr '):
                        current_msgstr = line[7:].strip('"')
                        in_msgid = False
                        in_msgstr = True
                    elif line.startswith('"') and line.endswith('"'):
                        val = line.strip('"')
                        if in_msgid:
                            current_msgid += val
                        elif in_msgstr:
                            current_msgstr += val
                            
                if current_msgid and current_msgstr:
                    translations[current_msgid] = current_msgstr
                    
                if "" in translations:
                    translations.pop("")
            except Exception as e:
                return Response({"detail": f"Error parsing po file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        return Response(translations)
