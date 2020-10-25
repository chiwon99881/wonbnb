from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "custom_input", "placeholder": "Email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "custom_input", "placeholder": "Password"}
        )
    )

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


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "custom_input", "placeholder": "First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "custom_input", "placeholder": "Last Name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "custom_input", "placeholder": "Email"}
            ),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "custom_input", "placeholder": "Password"}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "custom_input", "placeholder": "Confirm Password"}
        ),
        label="Confirm Password",
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("That email is already taken")
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

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        username = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = username
        user.set_password(password)
        user.save()


# View에서 Form으로 Form에 있는 Input data가 아닌 그 외의 data를 넘기는 방법
# __init__ 함수를 오버라이딩하여 View에서 Form을 부를때, pk 값을 넣어주어 그 pk값을 init함수에서 뽑아온다.
class ChangePasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop("pk", None)
        super().__init__(*args, **kwargs)

    current_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "custom_input", "placeholder": "Current Password"}
        )
    )
    change_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "custom_input", "placeholder": "Change Password"}
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "custom_input", "placeholder": "Confirm Password"}
        )
    )

    def clean_current_password(self):
        try:
            user = models.User.objects.get(pk=self.pk)
            current_password = self.cleaned_data.get("current_password")
            if user.check_password(current_password):
                return current_password
            else:
                self.add_error(
                    "current_password",
                    forms.ValidationError("Your current password was wrong."),
                )
        except models.User.DoesNotExist:
            self.add_error(None, forms.ValidationError("User Does not exist."))

    def clean_confirm_password(self):
        change_password = self.cleaned_data.get("change_password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if change_password == confirm_password:
            return change_password
        else:
            self.add_error(
                "confirm_password",
                forms.ValidationError(
                    "Confirm password is inconsistent with change password."
                ),
            )
