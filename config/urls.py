# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

# urlpatterns = [
#     path('admin/', admin.site.urls),
    
#     # JWT Auth Endpoints
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
#     # App API routes
#     path('', include('tickets.urls')),
#     path('', include('replies.urls')),
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# 👇 استيراد الـ TemplateView لقراءة واجهة Vue
from django.views.generic import TemplateView 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT Auth Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 👇 تعديل: جعل روابط التطبيقات تبدأ بـ api/ لمنع التداخل مع الفرونت اند
    path('api/', include('tickets.urls')),
    path('api/', include('replies.urls')),

    # 👇 السطر السحري: تشغيل واجهة Vue (index.html) عند الدخول للرابط الرئيسي للموقع مباشرة
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)