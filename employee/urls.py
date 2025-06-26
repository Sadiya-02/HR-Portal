from django.urls import path
from.import views
from employee import*

urlpatterns=[

    path('',views.index,name='home'),
    path('login/', views.employee_login, name='employee_login'),
    path('empdashboard',views.about,name='empdashboard'),   
    path('empprojects/', views.empprojects, name='empprojects'),
    path('upload/<int:project_id>/', views.upload_file, name='upload_file'),
    path('salary.html/',views.salary,name='salary'),
    path('todo/', views.emp_todo, name='emp_todolist'),
    path('todo/edit/<int:todo_id>/', views.edit_todo, name='edit_todo'),
    path('todo/delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('events/', views.view_events, name='employee_events'),
    path('attendance.html/',views.attendance,name='emp_attendance'),
    path('check-in/', views.check_in, name='check_in'),
    path('check-out/', views.check_out, name='check_out'),
    path('assigned-tickets/', views.assigned_tickets, name='assigned_tickets'),
    path('solve-ticket/<int:ticket_id>/', views.solve_ticket, name='solve_ticket'),
    path('leave-request/', views.leave_request_view, name='leave_request'),
    path('my-leave-request/', views.employee_leave_requests, name='leave_request_success'),
    path('my-tasks/', views.my_tasks, name='my-tasks'),
    path('notifications/', views.notification_page, name='employee_notifications'),
    path('calendar/events/', views.calendar_events, name='calendar_events'),
    path('my-salary-slips/', views.employee_salary_slips, name='employee_salary_slips'),
]