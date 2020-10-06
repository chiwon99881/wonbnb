from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [path("", views.HomeView.as_view(), name="all_rooms")]
