from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from django.utils import timezone
from . import models as room_models


class HomeView(ListView):

    """ HomeView Definition """

    model = room_models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    template_name = "rooms/home.html"
    template_name_suffix = ""
    context_object_name = "rooms"

    # 모든 Class Based View 는 get_context_data를 가진다.
    # context에 기존에 있는 값들에 + now 라는 값을 추가해준다.
    # 만약 첫번째 줄에 super()구문을 쓰지 않는다면 기존에 부모 클래스인 ListView가 가지고 있는
    # 모든 데이터들이 날라가므로 반드시 첫 줄에 작성해줘야 한다.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


class RoomDetail(DetailView):

    """ Room Detail Definition """

    model = room_models.Room


def search(request):

    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bathrooms = int(request.GET.get("bathrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    room_type = int(request.GET.get("room_type", 0))
    instant_book = request.GET.get("instant_book", False)
    super_host = request.GET.get("super_host", False)
    print(instant_book, super_host)
    # get() only 1, getlist() get list
    select_amenities = request.GET.getlist("amenities")
    select_facilities = request.GET.getlist("facilities")
    select_house_rules = request.GET.getlist("house_rules")

    form = {
        "city": city,
        "select_country": country,
        "select_room_type": room_type,
        "price": price,
        "guests": guests,
        "bathrooms": bathrooms,
        "beds": beds,
        "baths": baths,
        "select_amenities": select_amenities,
        "select_facilities": select_facilities,
        "select_house_rules": select_house_rules,
        "instant_book": instant_book,
        "super_host": super_host,
    }

    room_types = room_models.RoomType.objects.all()
    amenities = room_models.Amenity.objects.all()
    facilities = room_models.Facility.objects.all()
    house_rules = room_models.HouseRule.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
        "house_rules": house_rules,
    }

    return render(
        request,
        "rooms/search.html",
        context={**form, **choices},
    )
