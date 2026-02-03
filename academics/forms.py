from django import forms
from .models import Subject, Mark, Exam
from students.models import ClassDivision

class SubjectForm(forms.ModelForm):
    classes = forms.ModelMultipleChoiceField(
        queryset=ClassDivision.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = Subject
        fields = ['name', 'classes']
        widget = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

class MarksEntryForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['score']
        widgets = {
            'score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
        }

class AssignClassesForm(forms.ModelForm):
    classes = forms.ModelMultipleChoiceField(
        queryset=ClassDivision.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = Subject
        fields = ['classes']
