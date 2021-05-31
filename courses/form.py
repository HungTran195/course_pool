from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, AbstractUser


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")

    class Meta:
        model = User
        fields = ("email", "first_name",
                  "last_name", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email=email):
            return email
        else:
            raise forms.ValidationError('Email is used')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)

        user.email = self.cleaned_data["email"]
        user.username = user.email
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user
