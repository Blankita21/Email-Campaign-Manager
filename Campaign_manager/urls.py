from django.contrib import admin
from django.urls import path, include
from campaigns import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('campaigns/', include('campaigns.urls')),
]
