from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from . import models


class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['first_name', 'last_name','username','email','password1','password2']

class TeacherUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password']
        widgets={
            'password': forms.PasswordInput()
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model=models.Teacher
        fields=['first_name','last_name','department','semester_taught']


class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields = ['username','password']
        widgets={
            'password':forms.PasswordInput()
        }

class MarkForm(forms.Form):
    student=forms.ModelChoiceField(queryset=models.Student.objects.all())
    subject=forms.ModelChoiceField(queryset=models.Subject.objects.all())
    semester=forms.ModelChoiceField(queryset=models.Semester.objects.all())
    marks=forms.DecimalField(max_digits=5,decimal_places=2)

    def clean(self):
        cleaned_data=super().clean()
        student=cleaned_data.get('student')
        subject=cleaned_data.get('subject')
        semester=cleaned_data.get('semester')

        if models.Mark.objects.filter(student=student, subject=subject, semester=semester).exists():
            raise forms.ValidationError("Marks already assigned for this combination.")
        
        return cleaned_data





# It is removeable
class StudentForm(forms.ModelForm):
    class Meta:
        model=models.Student
        fields=['first_name','last_name','department','semesters_enrolled','subjects','registration_number']