import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import PrincipalRegistrationForm, PrincipalLoginForm, TeacherLoginForm

from .forms_teacher import AddTeacherForm, ChangeTeacherPasswordForm
from .models import User, Principal, Teacher
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
import datetime
from .decorators import principal_required, teacher_required







def landing_view(request):
    return render(request, 'landing.html')

def register_principal_view(request):
    if request.method == 'POST':
        form = PrincipalRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                if User.objects.filter(username=email).exists():
                     messages.error(request, "Account already exists.")
                     return redirect('login_principal')

                user = User.objects.create_user(username=email, email=email, password=password, role=User.Role.PRINCIPAL)
                Principal.objects.create(user=user)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
                messages.success(request, "Registration successful.")
                return redirect('principal_dashboard')
            except Exception as e:
                print(f"Registration Error: {e}")
                messages.error(request, f"Error creating account: {e}")
                return redirect('register_principal')
    else:
        form = PrincipalRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, 'title': 'Principal Registration'})

def login_principal_view(request):
    if request.user.is_authenticated:
        logout(request) # Force logout before new login attempt
        
    if request.method == 'POST':
        form = PrincipalLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                if user.role == User.Role.PRINCIPAL:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('principal_dashboard')
                else:
                    messages.error(request, "This account is not authorized as Principal.")
            else:
                 messages.error(request, "Invalid email or password.")
    else:
        form = PrincipalLoginForm()
    return render(request, 'accounts/login.html', {'form': form, 'title': 'Principal Login', 'type': 'Principal'})

def login_teacher_view(request):
    if request.user.is_authenticated:
        logout(request)
        
    if request.method == 'POST':
        form = TeacherLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user and user.role == User.Role.TEACHER:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('teacher_dashboard')
            else:
                messages.error(request, "Invalid username/password or not a teacher account.")
    else:
        form = TeacherLoginForm()
    return render(request, 'accounts/login.html', {'form': form, 'title': 'Teacher Login', 'type': 'Teacher'})



def logout_view(request):
    logout(request)
    return redirect('landing')

@login_required
@principal_required
def manage_teachers_view(request):
    principal = request.user.principal_profile
    teachers = Teacher.objects.filter(principal=principal, user__is_active=True)
    return render(request, 'principal/manage_teachers.html', {'teachers': teachers})

@login_required
@principal_required
def add_teacher_view(request):
    
    if request.method == 'POST':
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['full_name']
            password = form.cleaned_data['password']
            
            # Create User (Email is optional or we can set a dummy one if needed)
            # User model usually allows blank email, or we construct one: username@school.com
            email = f"{username}@school.internal" 
            
            try:
                # Create User
                user = User.objects.create_user(username=username, email=email, password=password, role=User.Role.TEACHER)
                user.first_name = name
                user.save()
                
                # Create Teacher Profile
                Teacher.objects.create(user=user, principal=request.user.principal_profile, phone='')
                
                messages.success(request, f"Teacher {name} added successfully.")
                return redirect('manage_teachers')
            except Exception as e:
                print(f"Error adding teacher: {e}")
                messages.error(request, f"Error: {e}")
    else:
        form = AddTeacherForm()
    
    return render(request, 'principal/add_teacher.html', {'form': form})

@login_required
@principal_required
def delete_teacher_view(request, teacher_id):
        
    teacher = get_object_or_404(Teacher, id=teacher_id, principal=request.user.principal_profile)
    
    # Requirement: Keeps historical data -> Soft Delete
    teacher.user.is_active = False
    teacher.user.save()
    
    messages.success(request, f"Teacher {teacher.user.username} has been deactivated.")
    return redirect('manage_teachers')

@login_required
@principal_required
def principal_dashboard_view(request):
    from students.models import Student, ClassDivision
    from academics.models import Subject
    
    context = {
        'teacher_count': Teacher.objects.filter(principal=request.user.principal_profile, user__is_active=True).count(),
        'student_count': Student.objects.count(),
        'class_count': ClassDivision.objects.count(),
        'subject_count': Subject.objects.count(),
    }
    return render(request, 'principal_dashboard.html', context)

@login_required
@teacher_required
def teacher_dashboard_view(request):
    return render(request, 'teacher_dashboard.html')

@login_required
@principal_required
def change_teacher_password_view(request, teacher_id):
    
    teacher = get_object_or_404(Teacher, id=teacher_id, principal=request.user.principal_profile)
    
    if request.method == 'POST':
        form = ChangeTeacherPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            teacher.user.set_password(new_password)
            teacher.user.save()
            messages.success(request, f"Password updated for {teacher.user.first_name}")
            return redirect('manage_teachers')
    else:
        form = ChangeTeacherPasswordForm()
        
    return render(request, 'principal/change_teacher_password.html', {'form': form, 'teacher': teacher})
