# customadmin/admin.py

from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from employee.forms import EmployeeForm
from employee.models import Employee
from .models import Todo
from .models import Attendance

# Custom admin view for adding employee
def add_employee_view(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)  # 👈 handle uploaded file
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

# Register the model and admin class
admin.site.register(Employee, CustomAdmin)
admin.site.register(Todo)
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'check_in', 'check_out')
    list_filter = ('user', 'date')
    search_fields = ('user__username',)

