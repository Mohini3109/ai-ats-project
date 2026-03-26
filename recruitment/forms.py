from django import forms
from .models import Candidate, Job

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['job', 'name', 'email', 'resume']
        widgets = {
            'job': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
        }

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'skills_required', 'experience']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Job Description'}),
            'skills_required': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'e.g. Python, Django, SQL'}),
            'experience': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2+ years'}),
        }
