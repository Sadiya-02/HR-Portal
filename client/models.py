from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='client_images/', blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)  # Add this

    def __str__(self):
        return self.user.username


class ClientProject(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='project_files/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Notification(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    message = models.CharField(max_length=255)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(ClientProject, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.message