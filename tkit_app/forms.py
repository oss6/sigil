from django import forms            
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm      


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user


class AddClassForm(forms.Form):
    name = forms.CharField(max_length=20)
    school = forms.CharField(max_length=20)
    description = forms.CharField(max_length=300)


class AddStudentForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(required=False)
    parent = forms.CharField(max_length=30)
    parent_email = forms.EmailField()
    photo = forms.ImageField(required=False)