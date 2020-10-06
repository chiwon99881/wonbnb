from django.views.generic import ListView
from . import models as room_models


class HomeView(ListView):

    """ HomeView Definition """

    model = room_models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    template_name = "rooms/home.html"
    template_name_suffix = ""
