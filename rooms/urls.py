from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>/", views.RoomDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", views.edit_room, name="edit"),
    path("<int:pk>/photos/", views.edit_photos, name="photos"),
    path("<int:pk>/photos/upload/", views.upload_photo, name="photo-upload"),
    path("search/", views.search, name="search"),
    path("photos/<int:pk>/delete/", views.delete_photo, name="photo-delete"),
    path("photos/<int:pk>/edit/", views.edit_photo_caption, name="photo-caption-edit"),
]
