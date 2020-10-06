from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from . import models as room_models


def all_rooms(request):
    # get() means key's value
    # ex) {page: ['1']}.get("page") => 1
    page = request.GET.get("page", 1)
    room_list = room_models.Room.objects.all()

    # paginator => Paginator
    paginator = Paginator(room_list, 10, orphans=5)
    # rooms => Paginator.page()
    # rooms.paginator => The associated Paginator Object like "paginator"
    try:
        rooms = paginator.page(int(page))
        return render(
            request,
            "rooms/home.html",
            context={"rooms": rooms},
        )
    except EmptyPage:
        return redirect("/")
