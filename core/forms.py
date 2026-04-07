from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Course, Assignment, Submission

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'role')

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'deadline', 'attachment']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class SubmissionGradeForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['grade', 'feedback']

class StudentSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']


