from django.db import models
from django.contrib.auth.models import User


    
class Todo(models.Model):
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)

    def _str_(self):
        return f"{self.user.username} - {self.date}"


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Assigned', 'Assigned'),
        ('Solved', 'Solved'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_tickets')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    assigned_employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    client_notification = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class EmployeeSolution(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Estimate(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='estimates/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True, null=True)

class Invoice(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='invoices/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class SalarySlip(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    slip_file = models.FileField(upload_to='salary_slips/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.username} - {self.month}"