from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import YearlyReport
from accounts.models import User, Teacher
from accounts.decorators import principal_required
from students.models import ClassDivision, Student
from academics.models import Mark, Exam, Subject
from attendance.models import AttendanceRecord
from .utils import generate_yearly_report_pdf
import datetime

@login_required
@principal_required
def generate_report_view(request):
    
    if request.method == 'POST':
        try:
            year = int(request.POST.get('year', datetime.datetime.now().year))
        except ValueError:
            messages.error(request, "Invalid year format.")
            return redirect('generate_report')
        
        # Gather Data
        principal = request.user.principal_profile
        teachers = Teacher.objects.select_related('user').all()
        classes_data = []
        
        # Optimize: Fetch all students once with their class
        all_students = Student.objects.select_related('class_division').all().order_by('class_division', 'roll_no')
        
        # Optimize: Fetch all marks once
        all_marks = Mark.objects.select_related('subject', 'exam').filter(student__in=all_students)
        marks_by_student = {}
        for m in all_marks:
            if m.student_id not in marks_by_student:
                marks_by_student[m.student_id] = []
            marks_by_student[m.student_id].append(m)
            
        # Optimize: Fetch attendance counts once
        from django.db.models import Count
        attendance_counts = AttendanceRecord.objects.filter(student__in=all_students, status='PRESENT')\
                            .values('student_id').annotate(count=Count('id'))
        attendance_by_student = {a['student_id']: a['count'] for a in attendance_counts}

        # Structure data
        classes = ClassDivision.objects.all().order_by('class_number', 'division')
        for cls in classes:
            cls_students = [s for s in all_students if s.class_division_id == cls.id]
            student_data = []
            for stud in cls_students:
                student_data.append({
                    'student': stud,
                    'marks': marks_by_student.get(stud.id, []),
                    'attendance_count': attendance_by_student.get(stud.id, 0)
                })
            
            classes_data.append({
                'class': cls,
                'students': student_data
            })
            
        # PDF Generation
        try:
             pdf_path = generate_yearly_report_pdf(year, principal, teachers, classes_data)
             YearlyReport.objects.create(principal=principal, year=year, pdf_file=pdf_path)
             messages.success(request, f"Report for year {year} generated successfully.")
             return redirect('view_reports')
        except Exception as e:
             messages.error(request, f"PDF Generation failed: {str(e)}")
             return redirect('generate_report')

    return render(request, 'reports/generate_report.html')

@login_required
@principal_required
def view_reports_view(request):
     
     # Get reports for the logged-in principal
     principal = request.user.principal_profile
     reports = YearlyReport.objects.filter(principal=principal).order_by('-created_at')
     return render(request, 'reports/view_reports.html', {'reports': reports})
