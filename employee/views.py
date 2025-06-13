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
from customadmin.models import Attendance
from datetime import datetime
from django.http import HttpResponse
import pytz
from customadmin.models import Ticket, EmployeeSolution
from customadmin.forms import EmployeeSolutionForm
from .forms import LeaveRequestForm
from .models import LeaveRequest
from client.models import Notification

# Create your views here.
def employee_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('empdashboard')  # Update this with your dashboard URL name
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'emp_login.html')

def index(request):
    return render(request, 'home.html')

@login_required
def about(request):
    user = request.user
    employee = Employee.objects.get(user=request.user)
    return render(request, 'emp_index.html', {'employee': employee})


# def emp_index(request):
#     return render(request, 'emp_index.html')# for redirect dashboard into dashboard

# def emp_project(request):
#     return render(request,'empproject.html')
# def empprojects(request):
#     projects = Project.objects.filter(assigned_to=request.user)
#     return render(request, 'empproject.html', {'projects': projects})

def empprojects(request):
    try:
        employee = Employee.objects.get(user=request.user)
        projects = employee.projects.all()
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

def events(request):
    return render(request,'events.html')




def task(request):
    return render(request,'task.html')

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
    todo = get_object_or_404(EmployeeTodo, id=todo_id, user=request.user)
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
    # today = datetime.now()
    formatted_date = today.strftime("%Y-%m-%d %H:%M:%S")
    existing = Attendance.objects.filter(user=request.user, date=today).first()

    if not existing:
        Attendance.objects.create(user=request.user, check_in=timezone.localtime(timezone.now()).time())
        # Attendance.objects.create(user=request.user, date=today, check_in=timezone(pytz.timezone("Asia/Kolkata")))   

    return redirect('emp_attendance')  # Or wherever you want

@login_required
def check_out(request):
    today = timezone.now().date()
    attendance = Attendance.objects.filter(user=request.user, date=today).first()

    if attendance and not attendance.check_out:
        attendance.check_out = timezone.localtime(timezone.now()).time()
        attendance.save()
    return redirect('emp_attendance')  # Or wherever you want
    
@login_required
def assigned_tickets(request):
    tickets = Ticket.objects.filter(assigned_employee=request.user, status='Assigned')
    return render(request, 'assigned_ticket.html', {'tickets': tickets})

@login_required
def solve_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, assigned_employee=request.user)
    if request.method == 'POST':
        form = EmployeeSolutionForm(request.POST)
        if form.is_valid():
            solution = form.save(commit=False)
            solution.ticket = ticket
            solution.employee = request.user
            solution.save()
            ticket.status = 'Solved'
            ticket.save()
            return redirect('assigned_tickets')
    else:
        form = EmployeeSolutionForm()
    return render(request, 'solve_ticketemp.html', {'form': form, 'ticket': ticket})

def leave_request_view(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user
            leave.save()
            Notification.objects.create(
                user=request.user,
                message="Your leave request has been submitted."
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
    return render(request, 'my_tasks.html', {'tasks': tasks})

