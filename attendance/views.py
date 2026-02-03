from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AttendanceSelectionForm
from .models import AttendanceSession, AttendanceRecord
from students.models import ClassDivision, Student
from accounts.models import User
from accounts.decorators import principal_or_teacher_required

@login_required
@principal_or_teacher_required
def take_attendance_view(request):
    
    if request.method == 'POST':
        # Stage 2: Save Attendance
        if 'save_attendance' in request.POST:
            class_id = request.POST.get('class_id')
            date = request.POST.get('date')
            cls = get_object_or_404(ClassDivision, id=class_id)
            
            # Create Session
            if request.user.role == User.Role.TEACHER:
                teacher = request.user.teacher_profile
            else:
                teacher = None # Principal taking attendance? Optional
            
            session, created = AttendanceSession.objects.get_or_create(date=date, class_division=cls, defaults={'teacher': teacher})
            
            # Save records
            students = cls.students.all()
            existing_records = {r.student_id: r for r in AttendanceRecord.objects.filter(session=session)}
            
            records_to_create = []
            records_to_update = []
            
            for student in students:
                status = request.POST.get(f'status_{student.id}', 'ABSENT')
                record = existing_records.get(student.id)
                if record:
                    if record.status != status:
                        record.status = status
                        records_to_update.append(record)
                else:
                    records_to_create.append(AttendanceRecord(session=session, student=student, status=status))
            
            if records_to_create:
                AttendanceRecord.objects.bulk_create(records_to_create)
            if records_to_update:
                AttendanceRecord.objects.bulk_update(records_to_update, ['status'])
            
            messages.success(request, f"Attendance processed for {len(records_to_create) + len(records_to_update)} students.")
            return redirect('teacher_dashboard')

        # Stage 1: Load Student List
        else:
             form = AttendanceSelectionForm(request.POST)
             if form.is_valid():
                 cls = form.cleaned_data['class_division']
                 date = form.cleaned_data['date']
                 students = cls.students.all().order_by('roll_no')
                 return render(request, 'attendance/take_attendance_list.html', {
                     'students': students, 
                     'class': cls, 
                     'date': date
                 })
    else:
        form = AttendanceSelectionForm()
    
    return render(request, 'attendance/select_class.html', {'form': form})
