from django import forms
from allauth.account.forms import SignupForm
from django.core.exceptions import ValidationError
from datetime import date
from .models import Profile

class CustomSignupForm(SignupForm):
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),label='Birthdate', required = True)
    def save(self, request):
        user = super().save(request)
        user.profile.birthdate = self.cleaned_data['birthdate']
        user.profile.save()
        return user


class CustomAuthorSignupForm(SignupForm):
    birthdate_author = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),label='Birthdate', required = True)

    def clean_birthdate_author(self):
        birthdate_checker = self.cleaned_data['birthdate_author']
        today = date.today()
        age = today.year - birthdate_checker.year - ((today.month, today.day) < (birthdate_checker.month, birthdate_checker.day))
        if age < 18:
            raise ValidationError("You must be at least 18 years old to sign up as an author.")
        return birthdate_checker

    def save(self, request):
        user = super().save(request)
        user.profile.birthdate_author = self.cleaned_data['birthdate_author']
        user.profile.save()
        return user
