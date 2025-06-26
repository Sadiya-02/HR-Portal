from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Project,Employee,Task
from django.contrib.auth.models import User
from .models import EmployeeTodo
from employee.models import Event
from django.utils import timezone
from django.views.decorators.http import require_POST
from customadmin.models import Attendance, Todo
from datetime import datetime
from django.http import HttpResponse
import pytz
from customadmin.models import Ticket, EmployeeSolution
from customadmin.forms import EmployeeSolutionForm
from .forms import LeaveRequestForm
from .models import LeaveRequest
from client.models import Notification,Client
from .models import EmployeeNotification
from datetime import date
from django.utils.safestring import mark_safe
import json
from django.http import JsonResponse
from customadmin.models import SalarySlip

# Create your views here.
def employee_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('empdashboard') 
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'emp_login.html')

def index(request):
    return render(request, 'home.html')

@login_required
def about(request):
    user = request.user
    employee = Employee.objects.get(user=user)
    pending_tasks = Task.objects.filter(assigned_to=user, completed=False).count()
    new_projects = Project.objects.filter(assigned_to=employee).count()
    client_count = Client.objects.count()
    

    return render(request, 'emp_index.html', {
        'employee': employee,
        'pending_tasks': pending_tasks,
        'new_projects':new_projects,
        'client_count': client_count,
    })


def empprojects(request):
    try:
        employee = Employee.objects.get(user=request.user)
        projects = employee.projects.all()
        admin_user = User.objects.filter(is_superuser=True).first()
        if admin_user:
            EmployeeNotification.objects.create(
                sender=request.user,
                receiver=admin_user,
                message=f"{request.user.first_name} viewed their assigned projects."
            )
        return render(request, 'empproject.html', {'projects': projects})
    except Employee.DoesNotExist:
        return HttpResponse("❌ You are not linked to an employee profile. Please contact the administrator.")
    
def upload_file(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST" and request.FILES.get("file"):
        project.uploaded_file = request.FILES["file"]
        project.save()
    return redirect('empprojects')

def attendance(request):
    return render(request,'emp_attendance.html')


def salary(request):
    return render(request,'salary.html')

def emp_todo(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        if task:
            EmployeeTodo.objects.create(user=request.user, task=task)
        return redirect('emp_todolist')

    todos = EmployeeTodo.objects.filter(user=request.user)
    edit_id = request.GET.get('edit_id')
    return render(request, 'todolist.html', {'todos': todos, 'edit_id': edit_id})

def edit_todo(request, todo_id):
    todo = get_object_or_404(EmployeeTodo, id=todo_id, user=request.user)
    if request.method == 'POST':
        task = request.POST.get('task')
        if task:
            todo.task = task
            todo.save()
    return redirect('emp_todolist')


def delete_todo(request, todo_id):
    if request.user.is_superuser:
        todo = get_object_or_404(Todo, id=todo_id)
        todo.delete()
        return redirect('todo_list')
    else:
        todo=get_object_or_404(EmployeeTodo,id=todo_id, user=request.user)
        todo.delete()
        return redirect('emp_todolist')

def view_events(request):
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(date__gte=today).order_by('date')
    past_events = Event.objects.filter(date__lt=today).order_by('-date')

    return render(request, 'view_eventsemp.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events
    })   

@login_required
def check_in(request):
    today = timezone.now().date()
    formatted_date = today.strftime("%Y-%m-%d %H:%M:%S")
    existing = Attendance.objects.filter(user=request.user, date=today).first()

    if not existing:
        Attendance.objects.create(user=request.user, check_in=timezone.localtime(timezone.now()).time())

    return redirect('emp_attendance')  

@login_required
def check_out(request):
    today = timezone.now().date()
    attendance = Attendance.objects.filter(user=request.user, date=today).first()

    if attendance and not attendance.check_out:
        attendance.check_out = timezone.localtime(timezone.now()).time()
        attendance.save()
    return redirect('emp_attendance')  
    
@login_required
def assigned_tickets(request):
    tickets = Ticket.objects.filter(assigned_employee=request.user, status='Assigned')
    return render(request, 'assigned_ticket.html', {'tickets': tickets})


@login_required
def solve_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, assigned_employee=request.user)
    
    
    try:
        existing_solution = EmployeeSolution.objects.get(ticket=ticket)
    except EmployeeSolution.DoesNotExist:
        existing_solution = None

    if request.method == 'POST':
        form = EmployeeSolutionForm(request.POST, instance=existing_solution)
        if form.is_valid():
            solution = form.save(commit=False)
            solution.ticket = ticket
            solution.employee = request.user
            solution.save()

            ticket.status = 'Solved'
            ticket.save()

            admin_user = User.objects.filter(is_superuser=True).first()
            if admin_user:
                EmployeeNotification.objects.create(
                    sender=request.user,
                    receiver=admin_user,
                    message=f"Ticket #{ticket.id} has been marked as solved by {request.user.username}."
                )
            return redirect('assigned_tickets')
    else:
        form = EmployeeSolutionForm(instance=existing_solution)

    return render(request, 'solve_ticketemp.html', {'form': form, 'ticket': ticket})

def leave_request_view(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user
            leave.save()

            
            admin_user = User.objects.filter(is_superuser=True).first()
            if admin_user:
                EmployeeNotification.objects.create(
                    sender=request.user,
                    receiver=admin_user,
                    message=f"{request.user.username} submitted a leave request from {leave.start_date} to {leave.end_date}."
                )

            return redirect('leave_request_success')  
    else:
        form = LeaveRequestForm()  

    return render(request, 'leave_request_form.html', {'form': form}) 

def employee_leave_requests(request):
    requests = LeaveRequest.objects.filter(employee=request.user)
    return render(request, 'manage_leave_requests.html', {'requests': requests})

def my_tasks(request):
    if request.user.is_superuser:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to=request.user)

        admin_user = User.objects.filter(is_superuser=True).first()
        if admin_user:
            EmployeeNotification.objects.create(
                sender=request.user,
                receiver=admin_user,
                message=f"{request.user.username} viewed their assigned tasks."
            )

    return render(request, 'my_tasks.html', {'tasks': tasks})

@login_required
def notification_page(request):
    notifications = EmployeeNotification.objects.filter(receiver=request.user).order_by('-created_at')
    return render(request, 'emp_notifications.html', {'notifications': notifications})

def calendar_events(request):
    events = []
    for event in Event.objects.all():
        events.append({
            'title': event.title,
            'start': event.date.strftime('%Y-%m-%d'),  
        })
    return JsonResponse(events, safe=False)

@login_required
def employee_salary_slips(request):
    slips = SalarySlip.objects.filter(employee=request.user).order_by('-uploaded_at')
    return render(request, 'salary.html', {'slips': slips})