from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [path("", views.all_rooms, name="all_rooms")]
