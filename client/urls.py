from django.urls import path
from.import views
from client import*

urlpatterns=[
    path('login/', views.client_login, name='client_login'),
    path('client_dashboard/',views.client_dashboard,name='client_dashboard'),
    path('raise-ticket/', views.raise_ticket, name='raise_ticket'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('add-project/', views.add_project, name='client_add_project'),
    path('projects/', views.view_projects, name='project_list'),
    path('estimates/', views.client_estimates, name='client_estimates'),
    path('estimate/<int:estimate_id>/respond/', views.respond_estimate, name='respond_estimate'),
    path('my-invoices/', views.client_invoices, name='client_invoices'),
]