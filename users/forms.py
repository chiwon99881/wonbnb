from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # clean method used when two field are related each others.
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)

            # check_password is a function provided by Django.
            if user.check_password(password):
                return self.cleaned_data
            else:
                # add_error is only used to just clean method
                # because should know to where this error occurs.
                self.add_error("password", forms.ValidationError("Password is wrong."))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist."))
