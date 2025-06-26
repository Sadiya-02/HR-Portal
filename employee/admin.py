# employee/admin.py

from django.contrib import admin
from .models import Employee, Project, Task
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import EmployeeTodo,Task
from django.utils.html import format_html


class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'Employee Info'
    fk_name = 'user'
    readonly_fields = ('uploaded_file_preview',)

    def uploaded_file_preview(self, obj):
        if obj.uploaded_file:
            return format_html("<a href='{}' target='_blank'>View File</a>", obj.uploaded_file.url)
        return "No file uploaded"
    uploaded_file_preview.short_description = "Uploaded File"


class CustomUserAdmin(UserAdmin):
    inlines = (EmployeeInline,)

    def employee_designation(self, obj):
        return obj.employee.designation if hasattr(obj, 'employee') else '-'
    employee_designation.short_description = 'Designation'

    def employee_date_of_joining(self, obj):
        return obj.employee.date_of_joining if hasattr(obj, 'employee') else '-'
    employee_date_of_joining.short_description = 'Date of Joining'

    list_display = UserAdmin.list_display + ('employee_designation', 'employee_date_of_joining',)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        formset.save_m2m()


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


admin.site.register(EmployeeTodo)
admin.site.register(Task)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client','assigned_to', 'uploaded_file')
    fields = ('name','client','description', 'assigned_to', 'start_date', 'end_date', 'uploaded_file')