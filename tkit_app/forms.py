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
    name = forms.CharField()
    school = forms.CharField()
    description = forms.CharField()


class AddStudentForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField(required=False)
    parent = forms.CharField()
    parent_email = forms.EmailField()
    photo = forms.ImageField(required=False)


class AddGradableItemForm(forms.Form):
    subject = forms.CharField()
    date = forms.DateField(required=False)
    type = forms.CharField()


class AddLessonForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()
    date = forms.DateField(required=False)


class AddAssignmentForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()
    date_begin = forms.DateField(required=False)
    date_end = forms.DateField()


class AddNoteForm(forms.Form):
    n_type = forms.CharField(max_length=1)
    date = forms.DateField()
    comment = forms.CharField()