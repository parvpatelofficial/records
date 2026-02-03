from django.db import models
from students.models import ClassDivision, Student
from accounts.models import Teacher

class AttendanceSession(models.Model):
    date = models.DateField()
    class_division = models.ForeignKey(ClassDivision, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('date', 'class_division')
    
    def __str__(self):
        return f"{self.date} - {self.class_division}"

class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
    ]
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='records')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student} - {self.status}"
