from django.db import models
from students.models import ClassDivision, Student
from accounts.models import Teacher

class Subject(models.Model):
    name = models.CharField(max_length=100)
    classes = models.ManyToManyField(ClassDivision, related_name='subjects')

    def __str__(self):
        return self.name

class Exam(models.Model):
    EXAM_TYPES = [
        ('UT1', 'Unit Test 1'),
        ('MID', 'Mid Term'),
        ('UT2', 'Unit Test 2'),
        ('FINAL', 'Final Exam'),
    ]
    name = models.CharField(max_length=10, choices=EXAM_TYPES, unique=True)
    
    def __str__(self):
        return self.get_name_display()

class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='marks')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    recorded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'subject', 'exam')

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.exam}: {self.score}"
