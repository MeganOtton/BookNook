from django import forms
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),label='Birthdate', required = True)
    def save(self, request):
        # user = super(CustomSignupForm, self).save(request)
        user = super().save(request)
        user.profile.birthdate = self.cleaned_data['birthdate']
        user.profile.save()
        return user


class CustomAuthorSignupForm(SignupForm):
    birthdate_author = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),label='Birthdate', required = True)
    def save(self, request):
        # user = super(CustomSignupForm, self).save(request)
        user = super().save(request)
        user.profile.birthdate_author = self.cleaned_data['birthdate_author']
        user.profile.save()
        return user
    