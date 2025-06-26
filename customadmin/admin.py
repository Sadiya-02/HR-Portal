

from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from employee.forms import EmployeeForm
from employee.models import Employee
from .models import Todo,ContactMessage
from .models import Attendance


def add_employee_view(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            return redirect('/admin/dashboard/add_employee/')
    else:
        form = EmployeeForm()

    return render(request, 'admin/add_employee.html', {'form': form})


class CustomAdmin(admin.ModelAdmin):
    change_list_template = 'admin/custom_admin.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add_employee/', self.admin_site.admin_view(add_employee_view))
        ]
        return custom_urls + urls


admin.site.register(Employee, CustomAdmin)
admin.site.register(Todo)
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'check_in', 'check_out')
    list_filter = ('user', 'date')
    search_fields = ('user__username',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'message', 'submitted_at')
    ordering = ['-submitted_at']