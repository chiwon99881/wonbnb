from django.shortcuts import render
from django.core.paginator import Paginator
from . import models as room_models


def all_rooms(request):
    # get() means key's value
    # ex) {page: ['1']}.get("page") => 1
    page = request.GET.get("page")
    room_list = room_models.Room.objects.all()

    # paginator => Paginator
    paginator = Paginator(room_list, 10)
    # rooms => Paginator.page()
    # rooms.paginator => The associated Paginator Object like "paginator"
    rooms = paginator.get_page(page)

    return render(
        request,
        "rooms/home.html",
        context={"rooms": rooms},
    )
