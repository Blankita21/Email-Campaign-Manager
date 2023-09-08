from django.urls import path
from . import views

urlpatterns = [
    path('admin/login/', views.admin_login, name='admin_login'),
    path('add_subscriber/', views.add_subscriber, name='add_subscriber'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('send_campaign/', views.send_campaign, name='send_campaign'),
]
