from django import forms
from .models import ClassDivision, Student

class ClassDivisionForm(forms.ModelForm):
    class Meta:
        model = ClassDivision
        fields = ['class_number', 'division', 'stream']
        widgets = {
            'class_number': forms.Select(attrs={'class': 'form-select'}),
            'division': forms.Select(attrs={'class': 'form-select'}),
            'stream': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        class_num = cleaned_data.get('class_number')
        stream = cleaned_data.get('stream')
        
        if class_num and int(class_num) < 11 and stream != 'NONE':
            self.add_error('stream', "Stream is only applicable for Class 11 and 12.")
        
        if class_num and int(class_num) >= 11 and stream == 'NONE':
             self.add_error('stream', "Stream is mandatory for Class 11 and 12.")
             
        return cleaned_data

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_no', 'class_division', 'address', 'parent_phone', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'roll_no': forms.TextInput(attrs={'class': 'form-control'}),
            'roll_no': forms.TextInput(attrs={'class': 'form-control'}),
            'class_division': forms.Select(attrs={'class': 'form-select', 'size': '7'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'parent_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
