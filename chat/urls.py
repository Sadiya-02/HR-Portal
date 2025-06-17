from django.urls import path, include
from chat import views as chat_views
from django.contrib.auth.views import LoginView, LogoutView


from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:room_name>/', views.chat_room, name='chat-room'),
    
    path('private/<str:username>/', views.private_chat, name='private-chat'),
    path('private/chats', views.private_chat, name='private-chat'),
    
    path('private/client/<str:username>/', views.chat_with_client, name='chat-with-client'),
    path('admin-client/chats', views.chat_with_client, name='chat-with-client'),
    
    path('private/emp/<str:username>/', views.chat_with_employee, name='chat-with-employee'),
    path('employee/chats', views.chat_with_employee, name='chat-with-employee'),
    
    
    path('private/adm/<str:username>/', views.chat_with_admin, name='chat-with-admin'),
    path('admin/chats', views.chat_with_admin, name='chat-with-admin'),
]
