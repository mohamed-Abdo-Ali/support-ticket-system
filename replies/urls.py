from django.urls import path
from . import views

app_name = 'replies'

urlpatterns = [
    path('add/<int:ticket_pk>/', views.add_reply, name='add_reply'),
    path('<int:pk>/edit/', views.edit_reply, name='edit_reply'),
    path('<int:pk>/delete/', views.delete_reply, name='delete_reply'),
]
