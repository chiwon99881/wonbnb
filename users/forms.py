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


class SignUpForm(forms.Form):

    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            user = models.User.objects.get(email=email)
            if user is not None:
                raise forms.ValidationError("This email already exists.")
        except models.User.DoesNotExist:
            return email

    # clean method executed sequentially so,
    # you do not use password, password1 variable in clean_password method
    # because password1 is below password so clean_password method don't understand password1
    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password doesn't match.")
        else:
            return password

    def save(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = models.User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
