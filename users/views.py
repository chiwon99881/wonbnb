import os
import requests
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms, models

# Compare FormView with View and Check what difference.


# No FormView
class LoginView(View):
    def get(self, request):
        form = forms.LoginForm()
        return render(request, "users/login.html", context={"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))
        return render(request, "users/login.html", context={"form": form})


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


# FormView
class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            user.verify_email()
        return super().form_valid(form)


def complete_verification(request, secret):

    try:
        user = models.User.objects.get(email_secret=secret)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add success message
    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


def github_callback(request):
    code = request.GET.get("code", None)
    client_id = os.environ.get("GH_ID")
    client_secret = os.environ.get("GH_SECRET")
    if code is not None:
        code_to_post = requests.post(
            f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
            headers={"Accept": "application/json"},
        )
        result_json = code_to_post.json()
        error = result_json.get("error", None)
        if error is not None:
            return redirect(reverse("core:home"))
        else:
            access_token = result_json.get("access_token")
            profile_request = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"token {access_token}",
                    "Accept": "application/json",
                },
            )
            profile_json = profile_request.json()
            username = profile_json.get("login", None)
            if username is not None:
                name = profile_json.get("name")
                email = profile_json.get("email")
                bio = profile_json.get("bio")
                check_user = models.User.objects.get(email=email)
                if check_user is not None:
                    return redirect(reverse("users:login"))
                else:
                    user = models.User.objects.create(
                        username=email, first_name=name, bio=bio, email=email
                    )
                    login(request, user)
                    return redirect(reverse("core:home"))
            else:
                return redirect(reverse("users:login"))
    else:
        return redirect(reverse("core:home"))
