from django.contrib import admin
from .models import Client
from .models import ClientProject, Notification



@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'company_description')

admin.site.register(ClientProject)
admin.site.register(Notification)
