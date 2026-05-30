from django.urls import path
from . import views

urlpatterns = [
    path('api/replies/', views.ReplyListCreateView.as_view(), name='reply-list-create'),
    path('api/replies/<int:pk>/', views.ReplyDetailView.as_view(), name='reply-detail'),
]
