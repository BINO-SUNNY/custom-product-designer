from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings
from .views import profile

urlpatterns = [
    path('change_order_status/<int:order_id>/', views.change_order_status, name='change_order_status'),
    path('designerdashboard',views.designerdashboard,name="designerdashboard"),
    path('allocated_jobs/',views.allocated_jobs, name='allocated_jobs'),
    path('completed_jobs/', views.completed_jobs, name='completed_jobs'),
    path('get-notifications/', views.get_notifications, name='get_notifications'),
    path('profile/', views.profile, name='profile'),    
    path('notify-design-requests/', views.notify_design_requests_list, name='notify_design_requests_list'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
