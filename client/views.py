from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Client
from customadmin.forms import TicketForm
from customadmin.models import Ticket
from .forms import ProjectForm
from .models import ClientProject, Notification
from customadmin.models import Estimate,Invoice
from django.utils import timezone


def client_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                user.username 
                login(request, user)
                return redirect('client_dashboard')
            except Client.DoesNotExist:
                messages.error(request, "You are not authorized as a client.")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'client_login.html')

@login_required
def client_dashboard(request):
    client = Client.objects.get(user=request.user)
    return render(request, 'client_dashboard.html', {'client': client})

@login_required
def raise_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.client = request.user
            ticket.save()
            return redirect('my_tickets')
    else:
        form = TicketForm()
    return render(request, 'raise_ticket.html', {'form': form})

@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(client=request.user)
    return render(request, 'client_tickets.html', {'tickets': tickets})

def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user
            project.save()
            Notification.objects.create(
                message=f"New project submitted: {project.title}",
                project=project,
                user=request.user
            )
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'client_add_project.html', {'form': form})

def view_projects(request):
    projects = ClientProject.objects.filter(client=request.user)
    return render(request, 'client_view_projects.html', {'projects': projects})

@login_required
def client_estimates(request):
    estimates = Estimate.objects.filter(client=request.user)
    return render(request, 'client_estimates.html', {'estimates': estimates})

@login_required
def respond_estimate(request, estimate_id):
    estimate = get_object_or_404(Estimate, id=estimate_id, client=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            estimate.status = 'approved'
            estimate.reviewed_at = timezone.now()
            estimate.save()

            Notification.objects.create(
                client=request.user,
                message=f"You approved estimate ID {estimate.id}",
                project=None  
            )

            return redirect('client_estimates')

        elif action == 'reject':
            reason = request.POST.get('rejection_reason')
            if not reason:
                return render(request, 'client_respond_estimate.html', {
                    'estimate': estimate,
                    'error': 'Rejection reason is required.',
                })

            estimate.status = 'rejected'
            estimate.rejection_reason = reason
            estimate.reviewed_at = timezone.now()
            estimate.save()

            Notification.objects.create(
                client=request.user,
                message=f"You rejected estimate ID {estimate.id}",
                project=None
            )

            return redirect('client_estimates')

    return render(request, 'client_respond_estimate.html', {'estimate': estimate})

@login_required
def client_invoices(request):
    invoices = Invoice.objects.filter(client=request.user)
    return render(request, 'client_view_invoices.html', {'invoices': invoices})


