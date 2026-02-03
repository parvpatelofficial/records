from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_report_view, name='generate_report'),
    path('view/', views.view_reports_view, name='view_reports'),
]
