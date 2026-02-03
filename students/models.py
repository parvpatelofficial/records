from django.db import models

class ClassDivision(models.Model):
    STREAM_CHOICES = [
        ('SCIENCE', 'Science'),
        ('COMMERCE', 'Commerce'),
        ('ARTS', 'Arts'),
        ('NONE', 'None'),
    ]
    
    class_number = models.IntegerField(choices=[(i, i) for i in range(1, 13)])
    division = models.CharField(max_length=1, choices=[(c, c) for c in 'ABCDEF'])
    stream = models.CharField(max_length=10, choices=STREAM_CHOICES, default='NONE', blank=True, null=True)

    class Meta:
        unique_together = ('class_number', 'division', 'stream')
        ordering = ['class_number', 'division']

    def __str__(self):
        s = f"{self.class_number}{self.division}"
        if self.stream and self.stream != 'NONE':
            s += f" ({self.stream})"
        return s

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20)
    class_division = models.ForeignKey(ClassDivision, on_delete=models.CASCADE, related_name='students')
    address = models.TextField(blank=True)
    parent_phone = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    
    class Meta:
        unique_together = ('roll_no', 'class_division')

    def __str__(self):
        return f"{self.name} ({self.class_division})"
