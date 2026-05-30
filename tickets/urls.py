from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tickets', views.TicketViewSet, basename='ticket')
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/dashboard/', views.DashboardView.as_view(), name='api_dashboard'),
    path('api/profile/', views.ProfileView.as_view(), name='api_profile'),
    path('api/register/', views.RegisterView.as_view(), name='api_register'),
    path('api/translations/<str:lang>/', views.TranslationView.as_view(), name='api_translations'),
]
