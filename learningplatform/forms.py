from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Course
from django.contrib.auth.forms import UserChangeForm


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role']  


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
