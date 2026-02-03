from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SubjectForm, MarksEntryForm, AssignClassesForm
from .models import Subject, Exam, Mark
from students.models import ClassDivision, Student
from accounts.models import User
from accounts.decorators import principal_or_teacher_required

@login_required
@principal_or_teacher_required
def add_subject_view(request):
     
     if request.method == 'POST':
          form = SubjectForm(request.POST)
          if form.is_valid():
               form.save()
               messages.success(request, "Subject added successfully.")
               return redirect('teacher_dashboard') # Or manage subjects
     else:
          form = SubjectForm()
     
     return render(request, 'academics/add_subject.html', {'form': form})

@login_required
@principal_or_teacher_required
def enter_marks_view(request):
     # Stage 2: Save Marks
     if request.method == 'POST' and 'save_marks' in request.POST:
          try:
               class_id = request.POST.get('class_id')
               subject_id = request.POST.get('subject_id')
               exam_name = request.POST.get('exam_name')
               
               cls = get_object_or_404(ClassDivision, id=class_id)
               subject = get_object_or_404(Subject, id=subject_id)
               
               if not cls.subjects.filter(id=subject_id).exists():
                    messages.error(request, "Subject is not assigned to this class.")
                    return redirect('enter_marks')
               
               exam, _ = Exam.objects.get_or_create(name=exam_name)
               
               students = cls.students.all()
               teacher_profile = getattr(request.user, 'teacher_profile', None) if request.user.role == User.Role.TEACHER else None

               marks_to_create = []
               marks_to_update = []
               
               # Fetch existing marks for this exam/subject/students to avoid N+1 queries
               existing_marks = {m.student_id: m for m in Mark.objects.filter(student__in=students, subject=subject, exam=exam)}

               for student in students:
                    score = request.POST.get(f'score_{student.id}')
                    if score and score.strip():
                         try:
                              score = float(score)
                              if score < 0 or score > 100:
                                   messages.warning(request, f"Score {score} for {student.name} is out of range (0-100).")
                                   continue
                         except ValueError:
                              messages.warning(request, f"Invalid score for {student.name}.")
                              continue
                         
                         existing_mark = existing_marks.get(student.id)
                         
                         if existing_mark:
                              if request.user.role == User.Role.TEACHER and existing_mark.recorded_by != teacher_profile:
                                   messages.warning(request, f"Cannot update mark for {student.name} (entered by another teacher).")
                                   continue
                              existing_mark.score = score
                              marks_to_update.append(existing_mark)
                         else:
                              marks_to_create.append(Mark(
                                   student=student,
                                   subject=subject,
                                   exam=exam,
                                   score=score,
                                   recorded_by=teacher_profile
                              ))
               
               if marks_to_create:
                    Mark.objects.bulk_create(marks_to_create)
               if marks_to_update:
                    Mark.objects.bulk_update(marks_to_update, ['score'])
               
               messages.success(request, f"Successfully processed {len(marks_to_create) + len(marks_to_update)} marks.")
               
               messages.success(request, "Marks updated successfully.")
               if request.user.role == User.Role.PRINCIPAL:
                    return redirect('principal_dashboard')
               return redirect('teacher_dashboard')
               
          except Exception as e:
               messages.error(request, f"Error saving marks: {e}")
               return redirect('teacher_dashboard')

     # Stage 1: Load Grid or Selection
     # Simple Flow: GET request with params = Grid, without params = Selection
     class_id = request.GET.get('class_id')
     subject_id = request.GET.get('subject_id')
     exam_name = request.GET.get('exam_name')
     
     if class_id and subject_id and exam_name:
          cls = get_object_or_404(ClassDivision, id=class_id)
          subject = get_object_or_404(Subject, id=subject_id)
          
          # Validate subject is assigned to this class
          if not cls.subjects.filter(id=subject_id).exists():
               messages.error(request, "Subject is not assigned to this class.")
               return redirect('enter_marks')
          
          students = cls.students.all().order_by('roll_no')
          
          # Fetch existing marks to populate grid
          exam, _ = Exam.objects.get_or_create(name=exam_name)
          marks_map = {}
          existing_marks = Mark.objects.filter(student__in=students, subject=subject, exam=exam)
          for m in existing_marks:
               marks_map[m.student.id] = m
          
          return render(request, 'academics/entry_grid.html', {
               'students': students,
               'class': cls,
               'subject': subject,
               'exam_name': exam_name,
               'exam_display': dict(Exam.EXAM_TYPES).get(exam_name, exam_name),
               'marks_map': marks_map
          })

     # Default: Selection Screen
     classes = ClassDivision.objects.all()
     
     # Improved: Filter subjects based on class if needed, or show all if nothing selected
     # For now, let's keep it simple but ensure subjects are prioritized if they are assigned to classes
     subjects = Subject.objects.all()
     exam_types = Exam.EXAM_TYPES
     
     return render(request, 'academics/select_exam.html', {
          'classes': classes,
          'subjects': subjects,
          'exam_types': exam_types
     })
@login_required
@principal_or_teacher_required
def assign_classes_view(request):
     
     subjects = Subject.objects.all()
     selected_subject = None
     form = None
     
     subject_id = request.GET.get('subject_id')
     if subject_id:
          selected_subject = get_object_or_404(Subject, id=subject_id)
          if request.method == 'POST':
               form = AssignClassesForm(request.POST, instance=selected_subject)
               if form.is_valid():
                    form.save()
                    messages.success(request, f"Classes assigned to {selected_subject.name} successfully.")
                    return redirect('assign_classes')
          else:
               form = AssignClassesForm(instance=selected_subject)
     
     return render(request, 'academics/assign_classes.html', {
          'subjects': subjects,
          'selected_subject': selected_subject,
          'form': form
     })
