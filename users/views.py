import os
import requests
from django.views import View
from django.views.generic import FormView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.contrib import messages
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
                messages.success(request, f"Welcome {user.first_name} 👊")
                login(request, user)
                return redirect(reverse("core:home"))
        return render(request, "users/login.html", context={"form": form})


def log_out(request):
    messages.success(request, "Logout success 🖐")
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


class GithubException(Exception):
    pass


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


def github_callback(request):
    try:
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
                raise GithubException("Can't authorized your github.")
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
                    try:
                        check_user = models.User.objects.get(email=email)
                        if check_user.login_method == models.User.LOGIN_GITHUB:
                            messages.success(
                                request, f"Welcome {check_user.first_name} 👊"
                            )
                            login(request, check_user)
                        else:
                            raise GithubException(
                                f"Please login with your {check_user.login_method}"
                            )
                    except models.User.DoesNotExist:
                        new_user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            bio=bio,
                            username=username,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        new_user.set_unusable_password()
                        new_user.save()
                        login(request, new_user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Something wrong. please wait 1 minutes.")
        else:
            raise GithubException("Can't authorized your github.")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class KakaoException(Exception):
    pass


def kakao_login(request):
    client_id = os.environ.get("KAKAO_API_KEY")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback/"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


def kakao_callback(request):
    try:
        code = request.GET.get("code", None)
        if code is not None:
            client_id = os.environ.get("KAKAO_API_KEY")
            redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback/"
            code_to_post = requests.post(
                f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}",
                headers={
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                    "Accept": "application/json",
                },
            )
            result_json = code_to_post.json()
            access_token = result_json.get("access_token", None)
            if access_token is not None:
                profile_get = requests.get(
                    "https://kapi.kakao.com/v2/user/me",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                        "Accept": "application/json",
                    },
                )
                profile = profile_get.json()
                print(profile)
                email = profile.get("kakao_account").get("email")
                name = profile.get("kakao_account").get("profile").get("nickname")
                # profile_image is URL
                profile_image = (
                    profile.get("kakao_account").get("profile").get("profile_image")
                )
                try:
                    check_user = models.User.objects.get(email=email)
                    if check_user.login_method == models.User.LOGIN_KAKAO:
                        messages.success(request, f"Welcome {check_user.first_name} 👊")
                        login(request, check_user)
                    else:
                        raise KakaoException(
                            f"Please login with your {check_user.login_method}"
                        )
                except models.User.DoesNotExist:
                    new_user = models.User.objects.create(
                        email=email,
                        username=email,
                        first_name=name,
                        login_method=models.User.LOGIN_KAKAO,
                        email_verified=True,
                    )
                    new_user.set_unusable_password()
                    new_user.save()
                    if profile_image is not None:
                        profile_image_request = requests.get(profile_image)
                        # ContentFile function changes "byte contents" to "file"
                        # file.content() means that byte.
                        new_user.avatar.save(
                            f"{name} - avatar",
                            ContentFile(profile_image_request.content),
                        )
                    login(request, new_user)
                return redirect(reverse("core:home"))
            else:
                raise KakaoException("You must agree email information.")
        else:
            raise KakaoException("Something wrong. please wait 1 minutes.")
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):

    model = models.User

    # context_object_name 이 의미하는 것은 현재 View가 클릭한 유저를 context에 담고
    # 그 유저를 뿌려주겠다는 의미
    context_object_name = "user_obj"


def user_profile_update(request, pk):

    user = models.User.objects.get(pk=pk)

    if request.method == "GET":
        return render(request, "users/user_update.html", context={"user": user})

    if request.method == "POST":
        update_avatar = request.FILES.get("avatar")
        update_first_name = request.POST.get("first_name")
        update_last_name = request.POST.get("last_name")
        update_bio = request.POST.get("bio")
        update_currency = request.POST.get("currency")

        try:
            user.first_name = update_first_name
            user.last_name = update_last_name
            user.bio = update_bio
            user.currency = update_currency
            user.avatar = update_avatar
            user.save()
            messages.success(request, "Update Complete 😘")
            return redirect(reverse("users:profile", kwargs={"pk": pk}))
        except Exception:
            messages.error(request, "Something is wrong 😥")
            return redirect(reverse("users:edit-profile", kwargs={"pk": pk}))


def user_password_update(request, pk):

    if request.method == "GET":
        form = forms.ChangePasswordForm()
        return render(request, "users/change_password.html", context={"form": form})

    if request.method == "POST":
        form = forms.ChangePasswordForm(request.POST, pk=pk)
        if form.is_valid():
            change_password = form.cleaned_data.get("change_password")
            try:
                user = models.User.objects.get(pk=pk)
                user.set_password(change_password)
                user.save()
                messages.success(request, "Success update password 😘")
                return redirect(reverse("users:edit-profile", kwargs={"pk": pk}))
            except models.User.DoesNotExist:
                messages.error(request, "Something is broken. please logout and reply.")
        return render(request, "users/change_password.html", context={"form": form})
