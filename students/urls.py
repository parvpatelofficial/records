from django.urls import path
from . import views

urlpatterns = [
    path('classes/', views.manage_classes_view, name='manage_classes'),
    path('students/', views.manage_students_view, name='manage_students'),
    path('students/add/', views.add_student_view, name='add_student'),
    path('students/edit/<int:student_id>/', views.edit_student_view, name='edit_student'),
    path('students/delete/<int:student_id>/', views.delete_student_view, name='delete_student'),
]
