from django import forms
from client.models import Client
from .models import Ticket, EmployeeSolution
from django.contrib.auth.models import User
from .models import Ticket
from employee.models import Task, Project
from .models import Estimate,Invoice


class AddClientForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    profile_image = forms.ImageField(required=True)


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'description']
        labels = {
            'subject': 'Project Name',
            'description': 'Issue',
        }
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class AssignTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['assigned_employee']
        labels = {
            'assigned_employee': 'Assign to Employee'
        }

    def __init__(self, *args, **kwargs):
        super(AssignTicketForm, self).__init__(*args, **kwargs)
        self.fields['assigned_employee'].queryset = User.objects.all()  # or use a custom filter
        self.fields['assigned_employee'].widget.attrs.update({'class': 'form-control'})

class EmployeeSolutionForm(forms.ModelForm):
    class Meta:
        model = EmployeeSolution
        fields = ['message']


class TaskAssignForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'assigned_to', 'description', 'submission_date']

    def __init__(self, *args, **kwargs):
        super(TaskAssignForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(is_superuser=False)

class EstimateForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields = ['client', 'file']

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client', 'title', 'file']