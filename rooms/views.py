from django.shortcuts import render
from . import models as room_models


def all_rooms(request):
    # get() means key's value
    # ex) {page: ['1']}.get("page") => 1
    page = request.GET.get("page", 1)
    page = int(page or 1)
    page_size = 10
    limit = page_size * page
    offset = limit - page_size

    all_rooms = room_models.Room.objects.all()[offset:limit]

    all_rooms_count = room_models.Room.objects.count()
    page_count = 0

    if all_rooms_count % 2 == 0:
        page_count = int(all_rooms_count / page_size)
    else:
        page_count = int(all_rooms_count / page_size) + 1

    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count + 1),
        },
    )
