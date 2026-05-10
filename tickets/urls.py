from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('tickets/new/', views.create_ticket, name='create_ticket'),
    path('tickets/<int:pk>/', views.ticket_detail, name='ticket_detail'), # [cite: 49]
    path('tickets/<int:pk>/edit/', views.edit_ticket, name='edit_ticket'), # [cite: 47]
    path('tickets/<int:pk>/delete/', views.delete_ticket, name='delete_ticket'),
    
    # User Management
    path('users/', views.user_list, name='user_list'),
    path('users/new/', views.user_create, name='user_create'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('profile/', views.profile, name='profile'),
]


