from django.shortcuts import render, get_object_or_404
from .models import ChatRoom, ChatMessage
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ChatRoom, ChatMessage
from client.models import Client
from employee.models import Employee
from .utils import get_or_create_private_chat

def chat_room(request, room_name):
    room = get_object_or_404(ChatRoom, name=room_name)
    messages = ChatMessage.objects.filter(room=room).order_by('timestamp')
    return render(request, 'chat/chat_room.html', {
        'room_name': room_name,
        'messages': messages,
    })
    
@login_required
def private_chat(request, username=None):
    """
    View for private messaging between the logged-in user and another user.
    """
    
    
    employees= User.objects.all()
    
    if username:          
        other_user = get_object_or_404(User, username=username)
        room = get_or_create_private_chat(request.user, other_user)
        messages = ChatMessage.objects.filter(room=room).order_by('timestamp')
    else :          
         room = None
         messages = None
         other_user = None

    return render(request, 'chat.html', {
        'room': room,
        'messages': messages,
        'other_user': other_user,
        'employees':employees
    })
    #chat/private_chat.html
    
@login_required
def chat_with_client(request, username=None):
    """
    View for private messaging between the logged-in user and another user.
    """
    
    
    clients= Client.objects.all()
    
    if username:          
        other_user = get_object_or_404(User, username=username)
        room = get_or_create_private_chat(request.user, other_user)
        messages = ChatMessage.objects.filter(room=room).order_by('timestamp')
    else :          
         room = None
         messages = None
         other_user = None

    return render(request, 'Client_Chat.html', {
        'room': room,
        'messages': messages,
        'other_user': other_user,
        'clients':clients
    })
    

@login_required
def chat_with_employee(request, username=None):
    """
    View for private messaging between the logged-in user and another user.
    """
    
    
    employees= Employee.objects.all().exclude(user=request.user)
    if username:          
        other_user = get_object_or_404(User, username=username)
        room = get_or_create_private_chat(request.user, other_user)
        messages = ChatMessage.objects.filter(room=room).order_by('timestamp')
    else :          
         room = None
         messages = None
         other_user = None

    return render(request, 'Employee_Chat.html', {
        'room': room,
        'messages': messages,
        'other_user': other_user,
        'employees':employees
    })
    #chat/private_chat.html
    
@login_required
def chat_with_admin(request, username=None):
    """
    View for private messaging between the logged-in user and another user.
    """
    
    
    admins= User.objects.filter(is_superuser=True)
    
    if username:          
        other_user = get_object_or_404(User, username=username)
        room = get_or_create_private_chat(request.user, other_user)
        messages = ChatMessage.objects.filter(room=room).order_by('timestamp')
    else :          
         room = None
         messages = None
         other_user = None

    return render(request, 'Admin_Chat.html', {
        'room': room,
        'messages': messages,
        'other_user': other_user,
        'admins':admins
    })
        

def get_user_role(user):
    if hasattr(user, 'client_profile'):
        return 'client'
    elif hasattr(user, 'profile'):
        return 'user'
    return None