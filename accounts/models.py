from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        PRINCIPAL = "PRINCIPAL", "Principal"
        TEACHER = "TEACHER", "Teacher"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.ADMIN)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Principal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='principal_profile')
    phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return self.user.username

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    principal = models.ForeignKey(Principal, on_delete=models.CASCADE, related_name='teachers')
    phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return self.user.username
