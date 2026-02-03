from django import forms
from students.models import ClassDivision

class AttendanceSelectionForm(forms.Form):
    class_division = forms.ModelChoiceField(queryset=ClassDivision.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
