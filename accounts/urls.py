from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('register/principal/', views.register_principal_view, name='register_principal'),
    path('login/principal/', views.login_principal_view, name='login_principal'),
    path('login/teacher/', views.login_teacher_view, name='login_teacher'),

    path('logout/', views.logout_view, name='logout'),
    
    # Principal Routes
    path('principal/teachers/', views.manage_teachers_view, name='manage_teachers'),
    path('principal/teachers/add/', views.add_teacher_view, name='add_teacher'),
    path('principal/teachers/delete/<int:teacher_id>/', views.delete_teacher_view, name='delete_teacher'),
    path('principal/teachers/password/<int:teacher_id>/', views.change_teacher_password_view, name='change_teacher_password'),
    
    # Placeholder dashboards
    # Placeholder dashboards
    path('dashboard/principal/', views.principal_dashboard_view, name='principal_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard_view, name='teacher_dashboard'),
]
