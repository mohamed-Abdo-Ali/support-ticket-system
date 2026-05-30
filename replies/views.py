from rest_framework import views, permissions, status
from rest_framework.response import Response
from tickets.models import Ticket
from .models import Reply
from .serializers import ReplySerializer

class ReplyListCreateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        ticket_id = request.query_params.get('ticket')
        if not ticket_id:
            return Response({"detail": "Ticket query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        ticket = Ticket.objects.filter(pk=ticket_id).first()
        if not ticket:
            return Response({"detail": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)
            
        if ticket.created_by != request.user and not request.user.is_staff:
            return Response({"detail": "You do not have permission to view replies for this ticket."}, status=status.HTTP_403_FORBIDDEN)
            
        replies = Reply.objects.filter(ticket=ticket).order_by('created_at')
        
        # Simple pagination if page query param is provided
        page = request.query_params.get('page')
        if page:
            from django.core.paginator import Paginator
            paginator = Paginator(replies, 5)
            try:
                page_obj = paginator.page(page)
                serializer = ReplySerializer(page_obj.object_list, many=True)
                return Response({
                    "results": serializer.data,
                    "count": paginator.count,
                    "has_next": page_obj.has_next(),
                    "has_previous": page_obj.has_previous(),
                    "num_pages": paginator.num_pages
                })
            except Exception as e:
                return Response({"detail": "Invalid page"}, status=status.HTTP_400_BAD_REQUEST)
                
        serializer = ReplySerializer(replies, many=True)
        return Response(serializer.data)

    def post(self, request):
        ticket_id = request.data.get('ticket')
        message = request.data.get('message')
        
        if not ticket_id:
            return Response({"detail": "Ticket ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not message or message.strip() == "":
            return Response({"detail": "Reply cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)
            
        ticket = Ticket.objects.filter(pk=ticket_id).first()
        if not ticket:
            return Response({"detail": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)
            
        if not request.user.is_staff or request.user.is_superuser:
            return Response({"detail": "Only support staff (not managers) can reply to tickets."}, status=status.HTTP_403_FORBIDDEN)
            
        if ticket.status == 'Closed':
            return Response({"detail": "Cannot reply to a closed ticket."}, status=status.HTTP_400_BAD_REQUEST)
            
        reply = Reply.objects.create(
            ticket=ticket,
            user=request.user,
            message=message
        )
        
        # Email Notification (simulated)
        try:
            from django.core.mail import send_mail
            send_mail(
                f'New Reply on Ticket #{ticket.id}',
                f'Hello,\n\nA support member has replied to your ticket: "{ticket.subject}".\n\nReply: {message}',
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@support.com',
                [ticket.created_by.email],
                fail_silently=True,
            )
        except:
            pass
            
        serializer = ReplySerializer(reply)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReplyDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        return Response({"detail": "Replies cannot be edited once posted for security and integrity."}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return Response({"detail": "Replies cannot be edited once posted for security and integrity."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        return Response({"detail": "Replies cannot be deleted once posted to maintain audit trail."}, status=status.HTTP_400_BAD_REQUEST)
