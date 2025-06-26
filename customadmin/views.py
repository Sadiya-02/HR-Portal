from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout 
from django.contrib import messages
from employee.forms import EmployeeForm  
from employee.models import Employee,Event,Project,LeaveRequest,Task 
from client.forms import ProjectForm
from django.contrib.admin.views.decorators import staff_member_required
from .models import Todo,ContactMessage
from .models import Attendance
from client.models import Client
from .forms import AddClientForm
from customadmin.models import Ticket, EmployeeSolution
from customadmin.forms import AssignTicketForm
from django.contrib.auth.decorators import login_required
from client.models import ClientProject
from .forms import TaskAssignForm
from django.http import HttpResponse
from .forms import EstimateForm,InvoiceForm
from .models import Estimate,Invoice
from django.utils import timezone
from datetime import date,timedelta,datetime
from django.utils import timezone
from django.db.models.functions import TruncMonth
from client.models import Notification as ClientNotification
from employee.models import EmployeeNotification
from django.utils import timezone
from itertools import chain
from operator import attrgetter
from .forms import SalarySlipForm
from .models import SalarySlip

def dashboard(request):
    return render(request,'dashboard.html')

def admin_login(request):
    try:
        if request.user.is_authenticated:
            return redirect('dashboard/')
        
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username = username)
            if not user_obj.exists ():
                messages.info(request, 'Account not found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            user_obj = authenticate(username = username, password = password)

            if user_obj and user_obj.is_superuser:
                login(request, user_obj)
                return redirect('dashboard/')
            
            messages.info(request, 'Invalid Password')
            return redirect('/')
        
        return render(request, 'login.html')
    
    except Exception as e:
        print(e)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            user = User.objects.create_user(username=username, password=password)
            user.is_staff = False  
            user.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('employee_login')  

    return render(request, 'add_employee.html')


def add_employee(request):
    if request.method == 'POST':
     
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        designation = request.POST.get('designation')
        date_of_joining = request.POST.get('date_of_joining')
        image = request.FILES.get('image')  

        try:
            
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken. Please choose another.")
                return redirect('add_employee')

            
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )

            
            employee = Employee.objects.create(
                user=user,
                phone=phone,
                designation=designation,
                date_of_joining=date_of_joining)
            if image:
                employee.image=image 
                employee.save()
            else:
                messages.error("couldn't Upload profile pic of employee")
            messages.success(request, "Employee registered successfully!")
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")

        return redirect('add_employee') 

    return render(request, 'add_employee.html')



def todo_list(request):
    todos = Todo.objects.all()  
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Todo.objects.create(title=title)
        return redirect('todo_list')
    return render(request, 'todo_adm.html', {'todos': todos})

def toggle_task(request, task_id):
    todo = Todo.objects.get(id=task_id)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')


def delete_task(request, task_id):
    task = get_object_or_404(Todo, id=task_id)
    task.delete()
    return redirect('todo_list')


def add_project(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        employee_id = request.POST.get('employee')  
        client_id = request.POST.get('client')  
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        uploaded_file = request.FILES.get('project_file')  

        try:
            assigned_to = Employee.objects.get(id=employee_id)
            client = Client.objects.get(id=client_id)

            project=Project.objects.create(
                name=name,
                description=description,
                assigned_to=assigned_to,
                start_date=start_date,
                end_date=end_date,
                client =client,
                
            )
            if uploaded_file:
                project.uploaded_file=uploaded_file
                project.save()
                
            EmployeeNotification.objects.create(
                sender=request.user,
                receiver=assigned_to.user, 
                message=f"You have been assigned a new project: '{project.name}'."
            )

            return redirect('projectList')  

        except Employee.DoesNotExist:
            return render(request, 'add_project.html', {
                'employees': Employee.objects.all(),
                'error': 'Employee not found.'
            })

    employees = Employee.objects.all()
    return render(request, 'add_project.html', {'employees': employees,'clients': Client.objects.all(),})

def add_event(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        date = request.POST.get("date")

        Event.objects.create(title=title, description=description, date=date)
        messages.success(request, "Event added successfully.")
        return redirect("add_event")

    events = Event.objects.all().order_by('-created_at')  
    return render(request, "add_event.html", {"events": events})

def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.description = request.POST.get('description')
        event.date = request.POST.get('date')
        event.time = request.POST.get('time')
        event.location = request.POST.get('location')
        event.save()
        messages.success(request, "Event updated successfully.")
        return redirect('add_event')

    return render(request, 'edit_event.html', {'event': event})


def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    messages.success(request, "Event deleted successfully.")
    return redirect('add_event')

def email_view(request):
    return render(request,'email.html')

def see_employees(request):
    employees = Employee.objects.all()
    return render(request, 'see_employees.html', {'employees': employees})

def see_clients(request):
    clients = Client.objects.all()
    return render(request, 'see_client.html', {'clients': clients})

@staff_member_required
def attendance_list(request):
    attendance_records = Attendance.objects.select_related('user').order_by('-date')
    return render(request, 'attendance_list.html', {'attendance_records': attendance_records})


def add_client(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        profile_image = request.FILES.get('profile_image')
        company_name = request.POST.get('company_name')  # New
        company_description = request.POST.get('company_description')  # New

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('add_client')

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            # 
            Client.objects.create(
                user=user,
                profile_image=profile_image,
                company_name=company_name,
                company_description=company_description
            )

            messages.success(request, "Client added successfully.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('see_client')

        return redirect('add_client')

    return render(request, 'add_client.html')

def logoutPage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged Out Successfully")
        return redirect('/')
    return redirect('/')

@login_required
def admin_view_tickets(request):
    tickets = Ticket.objects.all()
    return render(request, 'view_ticketsadmin.html', {'tickets': tickets})

@login_required
def assign_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = AssignTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket.status = 'Assigned'
            form.save()
            
            assigned_employee = ticket.assigned_employee  
            if assigned_employee:
                EmployeeNotification.objects.create(
                    sender=request.user,
                    receiver=assigned_employee,
                    message=f"You have been assigned ticket #{ticket.id}: {ticket.subject}"
                )
            return redirect('view_tickets')
    else:
        form = AssignTicketForm(instance=ticket)
    return render(request, 'assign_ticket.html', {'form': form, 'ticket': ticket})
    
@login_required
def forward_solution_to_client(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    solution = get_object_or_404(EmployeeSolution, ticket=ticket)
    ticket.client_notification = f"Ticket successfully cleared. Message: {solution.message}"
    ticket.save()
    return redirect('admin_view_tickets')

def view_tickets(request):
    tickets = Ticket.objects.all()
    return render(request, 'view_tickets.html', {'tickets': tickets})


def admin_project_list(request):
    projects = ClientProject.objects.all().order_by('-created_at')
    return render(request, 'client_project_list.html', {'projects': projects})


@login_required
def notifications_view(request):
    
    if not request.user.is_staff:
        return redirect('home')  
    client_notifications = ClientNotification.objects.all()
    employee_notifications = EmployeeNotification.objects.filter(receiver=request.user)

    combined_notifications = sorted(
        chain(client_notifications, employee_notifications),
        key=attrgetter('created_at'),
        reverse=True
    )

    return render(request, 'notifications.html', {
        'notifications': combined_notifications
    })

def edit_client_project(request, project_id):
    project = get_object_or_404(ClientProject, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project) 
        if form.is_valid():
            print(form.data)
            updated_project = form.save()
            print(updated_project.status)
            ClientNotification.objects.create(
                message=f"Project updated: {updated_project.title}",
                project=updated_project
            )
            return redirect('admin_project_list')  
    else:
        form = ProjectForm(instance=project)  
        return render(request, 'client_add_project.html', {'form': form})
    
    return redirect('admin_project_list')

def manage_leave_requests(request):
    requests = LeaveRequest.objects.all()
    return render(request, 'manage_leave_requests.html', {'requests': requests})

def handle_leave_request(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            leave.status = 'Approved'
            leave.rejection_reason = ''
            leave.save()

  
            EmployeeNotification.objects.create(
                sender=request.user,
                receiver=leave.employee,  
                message="Your leave request has been approved."
            )


        elif action == 'reject':
            leave.status = 'Rejected'
            leave.rejection_reason = request.POST.get('rejection_reason', '')
            leave.save()

          
            EmployeeNotification.objects.create(
                sender=request.user,
                receiver=leave.employee,
                message=f"Your leave request has been rejected. Reason: {leave.rejection_reason}"
            )
       
        return redirect('manage_leave_requests')
    return render(request, 'handle_leave_request.html', {'leave': leave})


def assign_task(request):
    if request.method == 'POST':
        form = TaskAssignForm(request.POST)
        if form.is_valid():
            task = form.save()
            EmployeeNotification.objects.create(
                sender=request.user,
                receiver=task.assigned_to, 
                message=f"You have been assigned a new task for project: {task.project.name}."
            )
            return redirect('assign-task')
    else:
        form = TaskAssignForm()
    return render(request, 'assign_task.html', {'form': form})


def update_task_status(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        task = get_object_or_404(Task, id=task_id)
    
        if 'task_check' in request.POST:
            task.completed = True
            messages.success(request, 'Task marked as completed!')
            task.save()
        return redirect('my-tasks') 
    
def adminprojects(request):
    if request.user.is_superuser :
        projects = Project.objects.all()
        return render(request, 'projectList.html', {'projects': projects})
    else :
        return HttpResponse("You are not linked to an admin.")

@login_required
def add_estimate(request):
    if request.method == 'POST':
        form = EstimateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_estimates')
    else:
        form = EstimateForm()
    return render(request, 'adm_add_estimate.html', {'form': form})

@login_required
def view_estimates(request):
    estimates = Estimate.objects.all()
    return render(request, 'adm_view_estimates.html', {'estimates': estimates})

@login_required
def estimate_review(request, estimate_id):
    estimate = get_object_or_404(Estimate, id=estimate_id)
    return render(request, 'adm_estimate_review.html', {'estimate': estimate})

@login_required
def upload_invoice(request):
    invoices = Invoice.objects.all()
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_invoice')
    else:
        form = InvoiceForm()
    
    return render(request, 'adm_upload_invoice.html', {'form': form, 'invoices': invoices})


@login_required
def view_all_invoices_admin(request):
    invoices = Invoice.objects.all()
    return render(request, 'adm_all_invoices.html', {'invoices': invoices})


def attendance_data(request):

    selected_date = request.GET.get('date')
    
    if selected_date:
        try:
            selected_date = date.fromisoformat(selected_date)
        except (ValueError, TypeError):
            selected_date = timezone.now().date()
    else:
        selected_date = timezone.now().date()
    

    attendances = Attendance.objects.filter(date=selected_date).select_related('user')
    
    context = {
        'selected_date': selected_date,
        'attendances': attendances,
    }
    
    return render(request, 'attendence_data.html', context)


def attendance_report(request):
    if not request.user.is_authenticated:
        
        pass
    
    current_user = request.user
    today = timezone.now().date()
    selected_month = request.GET.get('month')
    

    week_start = today - timedelta(days=7)
    weekly_attendances = Attendance.objects.filter(
        user=current_user,
        date__gte=week_start
    ).order_by('-date')
    

    all_available_months = Attendance.objects.filter(
        user=current_user
    ).annotate(
        month=TruncMonth('date')
    ).values_list('month', flat=True).distinct().order_by('-month')
    

    if selected_month:
        try:
            selected_date = datetime.strptime(selected_month, '%Y-%m').date()
            month_start = selected_date.replace(day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            attendances = Attendance.objects.filter(
                user=current_user,
                date__gte=month_start,
                date__lte=month_end
            ).order_by('-date')
            
            monthly_data = [{
                'month_start': month_start,
                'month_end': month_end,
                'attendances': attendances,
                'month_name': month_start.strftime("%B %Y"),
                'is_current': (month_start.month == today.month and 
                              month_start.year == today.year)
            }]
        except ValueError:
            monthly_data = []
    else:
        
        monthly_data = []
        for month in all_available_months:
            month_start = month
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            attendances = Attendance.objects.filter(
                user=current_user,
                date__gte=month_start,
                date__lte=month_end
            ).order_by('-date')
            
            monthly_data.append({
                'month_start': month_start,
                'month_end': month_end,
                'attendances': attendances,
                'month_name': month_start.strftime("%B %Y"),
                'is_current': (month_start.month == today.month and 
                              month_start.year == today.year)
            })
    
    context = {
        'current_user': current_user,
        'weekly_attendances': weekly_attendances,
        'monthly_data': monthly_data,
        'all_available_months': all_available_months,
        'selected_month': selected_month,
        'current_month': today,
        'week_start': week_start,
        'today': today,
    }
    return render(request, 'report.html', context)

def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        if name and email and phone and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message
            )
            messages.success(request, "Your message has been sent.")
        else:
            messages.error(request, "All fields are required.")

    return redirect('home')  

@staff_member_required
def contact_messages_view(request):
    messages = ContactMessage.objects.order_by('-submitted_at')
    return render(request, 'admin_view_messages.html', {'messages': messages})

@login_required
def upload_salary_slip(request):
    if request.method == 'POST':
        form = SalarySlipForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('salary_slip_list_admin')  
    else:
        form = SalarySlipForm()
    return render(request, 'upload_salary_slip.html', {'form': form})

@login_required
def salary_slip_list_admin(request):
    slips = SalarySlip.objects.all().order_by('-uploaded_at')
    return render(request, 'salary_slip_list_admin.html', {'slips': slips})
