# import operator
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from . import models as room_models
from . import forms
import time


class HomeView(ListView):

    """ HomeView Definition """

    model = room_models.Room
    paginate_by = 12
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

    country = request.GET.get("country")
    header_city = request.GET.get("city")

    print(header_city)

    if country:

        form = forms.SearchForm(request.GET)

        if form.is_valid():
            city = form.cleaned_data.get("city")
            country = form.cleaned_data.get("country")
            room_type = form.cleaned_data.get("room_type")
            price = form.cleaned_data.get("price")
            guests = form.cleaned_data.get("guests")
            bedrooms = form.cleaned_data.get("bedrooms")
            baths = form.cleaned_data.get("baths")
            beds = form.cleaned_data.get("beds")
            instant_book = form.cleaned_data.get("instant_book")
            superhost = form.cleaned_data.get("superhost")
            amenities = form.cleaned_data.get("amenities")
            facilities = form.cleaned_data.get("facilities")
            house_rules = form.cleaned_data.get("house_rules")
            filter_args = {}

            if city != "Anywhere":
                filter_args["city__istartswith"] = city
            if country is not None:
                filter_args["country"] = country
            if room_type is not None:
                filter_args["room_type"] = room_type
            if price is not None:
                filter_args["price__lte"] = price
            if guests is not None:
                filter_args["guests__gte"] = guests
            if bedrooms is not None:
                filter_args["bedrooms__gte"] = bedrooms
            if baths is not None:
                filter_args["baths__gte"] = baths
            if beds is not None:
                filter_args["beds__gte"] = beds
            if instant_book is True:
                filter_args["instant_book"] = True
            if superhost is True:
                filter_args["host__superhost"] = True

            qs = room_models.Room.objects.filter(**filter_args)

            if amenities is not None:
                for amenity in amenities:
                    qs = qs.filter(amenity=amenity)
            if facilities is not None:
                for facility in facilities:
                    qs = qs.filter(facility=facility)
            if house_rules is not None:
                for rules in house_rules:
                    qs = qs.filter(house_rules=rules)

            qs = qs.order_by("-created")

            paginator = Paginator(qs, 10, orphans=5)

            page = request.GET.get("page", 1)

            rooms = paginator.get_page(page)

            return render(
                request,
                "rooms/search.html",
                context={"form": form, "rooms": rooms},
            )
    elif header_city is not None and country is None:
        header_city = str.capitalize(header_city)
        form = forms.SearchForm(data={"city": header_city})

        qs = room_models.Room.objects.filter(city=header_city).order_by("-created")

        paginator = Paginator(qs, 10, orphans=5)

        page = request.GET.get("page", 1)

        rooms = paginator.get_page(page)

        return render(
            request,
            "rooms/search.html",
            context={"form": form, "rooms": rooms},
        )
    else:
        form = forms.SearchForm()
    return render(
        request,
        "rooms/search.html",
        context={"form": form},
    )


def edit_room(request, pk):

    room = room_models.Room.objects.get(pk=pk)

    if request.method == "GET":
        if request.user != room.host:
            return redirect(reverse("core:home"))

        room_name = room.name
        room_desc = room.description
        room_country = room.country
        room_city = room.city
        room_price = room.price
        room_address = room.address
        room_guests = room.guests
        room_beds = room.beds
        room_bedrooms = room.bedrooms
        room_baths = room.baths
        room_check_in = room.check_in
        room_check_out = room.check_out
        room_instant_book = room.instant_book
        room_room_type = room.room_type
        room_amenity = room.amenity.all()
        room_facility = room.facility.all()
        room_house_rules = room.house_rules.all()
        form = forms.EditRoomForm(
            data={
                "name": room_name,
                "description": room_desc,
                "country": room_country,
                "city": room_city,
                "price": room_price,
                "address": room_address,
                "guests": room_guests,
                "beds": room_beds,
                "bedrooms": room_bedrooms,
                "baths": room_baths,
                "check_in": room_check_in,
                "check_out": room_check_out,
                "instant_book": room_instant_book,
                "room_type": room_room_type,
                "amenity": room_amenity,
                "facility": room_facility,
                "house_rules": room_house_rules,
            }
        )
        return render(
            request, "rooms/room_edit.html", context={"form": form, "room": room}
        )

    if request.method == "POST":
        form = forms.EditRoomForm(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data.get("name")
            new_desc = form.cleaned_data.get("description")
            new_country = form.cleaned_data.get("country")
            new_city = form.cleaned_data.get("city")
            new_price = form.cleaned_data.get("price")
            new_address = form.cleaned_data.get("address")
            new_guests = form.cleaned_data.get("guests")
            new_beds = form.cleaned_data.get("beds")
            new_bedrooms = form.cleaned_data.get("bedrooms")
            new_baths = form.cleaned_data.get("baths")
            new_check_in = form.cleaned_data.get("check_in")
            new_check_out = form.cleaned_data.get("check_out")
            new_instant_book = form.cleaned_data.get("instant_book")
            new_room_type = form.cleaned_data.get("room_type")
            new_amenity = form.cleaned_data.get("amenity")
            new_facility = form.cleaned_data.get("facility")
            new_house_rules = form.cleaned_data.get("house_rules")

            room.name = new_name
            room.description = new_desc
            room.country = new_country
            room.city = new_city
            room.price = new_price
            room.address = new_address
            room.guests = new_guests
            room.beds = new_beds
            room.bedrooms = new_bedrooms
            room.baths = new_baths
            room.check_in = new_check_in
            room.check_out = new_check_out
            room.instant_book = new_instant_book
            room.room_type = new_room_type
            room.amenity.set(new_amenity)
            room.facility.set(new_facility)
            room.house_rules.set(new_house_rules)
            try:
                room.save()
                messages.success(request, "Room Updated Completely 😍")
                return redirect(reverse("rooms:detail", kwargs={"pk": pk}))
            except Exception:
                messages.error(request, "Something wrong.. please again later 😥")
                return render(request, "rooms/room_edit.html", context={"form": form})


def edit_photos(request, pk):

    room = room_models.Room.objects.get(pk=pk)

    if request.method == "GET":
        if request.user != room.host:
            return redirect(reverse("core:home"))
        else:
            return render(request, "rooms/room_photos.html", context={"room": room})


@login_required
def delete_photo(request, pk):

    photo = room_models.Photo.objects.get(pk=pk)

    if request.method == "GET":
        if photo.room.host != request.user:
            return redirect(reverse("core:home"))
        else:
            try:
                photo.delete()
                messages.success(request, "Photo delete completely 😊")
                time.sleep(2)
            except Exception:
                messages.error(request, "Something is wrong.. please try it later 😥")
            return redirect(reverse("rooms:photos", kwargs={"pk": photo.room.pk}))
    else:
        return redirect(reverse("rooms:photos", kwargs={"pk": photo.room.pk}))


@login_required
def edit_photo_caption(request, pk):

    if request.method == "GET":
        try:
            photo = room_models.Photo.objects.get(pk=pk)
            if photo.room.host != request.user:
                return redirect(reverse("core:home"))
            else:
                return render(
                    request, "rooms/photos/photo_edit.html", context={"photo": photo}
                )
        except room_models.Photo.DoesNotExist:
            return redirect(reverse("core:home"))

    if request.method == "POST":

        new_caption = request.POST.get("caption")
        if new_caption is not None:
            try:
                photo = room_models.Photo.objects.get(pk=pk)
                if request.user != photo.room.host:
                    return redirect(reverse("core:home"))
                else:
                    photo.caption = new_caption
                    photo.save()
                    messages.success(request, "Edit caption completely 😊")
                    return redirect(
                        reverse("rooms:photos", kwargs={"pk": photo.room.pk})
                    )
            except room_models.Photo.DoesNotExist:
                return redirect(reverse("core:home"))


@login_required
def upload_photo(request, pk):

    room = room_models.Room.objects.get(pk=pk)

    if request.method == "GET":
        if room.host != request.user:
            return redirect(reverse("core:home"))
        else:
            return render(request, "rooms/photos/photo_upload.html")

    if request.method == "POST":
        if request.user != room.host:
            return redirect(reverse("core:home"))
        else:
            caption = request.POST.get("caption")
            file = request.FILES.get("file")

            if caption is None:
                messages.warning(request, "Caption is Required. 😥")
                return redirect(reverse("rooms:photo-upload", kwargs={"pk": pk}))
            elif file is None:
                messages.warning(request, "Room Photo is Required. 😥")
                return redirect(reverse("rooms:photo-upload", kwargs={"pk": pk}))
            else:
                try:
                    room_models.Photo.objects.create(
                        caption=caption, file=file, room=room
                    )
                    messages.success(request, "Photo uploaded 🥰")
                    return redirect(reverse("rooms:photos", kwargs={"pk": pk}))
                except Exception:
                    messages.error(request, "Create Error please try again later. 😥")
                    return redirect(reverse("rooms:photo-upload", kwargs={"pk": pk}))


def create_room(request):

    if request.method == "GET":
        form = forms.CreateRoomForm()
        return render(request, "rooms/room_create.html", context={"form": form})

    if request.method == "POST":
        form = forms.CreateRoomForm(request.POST)
        if form.is_valid():

            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            country = form.cleaned_data.get("country")
            city = form.cleaned_data.get("city")
            price = form.cleaned_data.get("price")
            address = form.cleaned_data.get("address")
            guests = form.cleaned_data.get("guests")
            beds = form.cleaned_data.get("beds")
            bedrooms = form.cleaned_data.get("bedrooms")
            baths = form.cleaned_data.get("baths")
            check_in = form.cleaned_data.get("check_in")
            check_out = form.cleaned_data.get("check_out")
            room_type = form.cleaned_data.get("room_type")
            instant_book = form.cleaned_data.get("instant_book")
            amenity = form.cleaned_data.get("amenity")
            facility = form.cleaned_data.get("facility")
            house_rules = form.cleaned_data.get("house_rules")

            try:
                create_room = room_models.Room.objects.create(
                    name=name,
                    host=request.user,
                    description=description,
                    country=country,
                    city=city,
                    price=price,
                    address=address,
                    guests=guests,
                    beds=beds,
                    bedrooms=bedrooms,
                    baths=baths,
                    check_in=check_in,
                    check_out=check_out,
                    room_type=room_type,
                    instant_book=instant_book,
                )
                create_room.amenity.set(amenity)
                create_room.facility.set(facility)
                create_room.house_rules.set(house_rules)
                messages.success(request, "Create room completely 😍")
                return redirect(reverse("rooms:detail", kwargs={"pk": create_room.pk}))
            except Exception as e:
                print(e)
                messages.error(request, "Something wrong while creating room. 😥")
                return render(request, "rooms/room_create.html", context={"form": form})


@login_required
def delete_room(request, pk):
    room = room_models.Room.objects.get(pk=pk)
    room_host = room.host

    if request.user != room_host:
        return redirect(reverse("core:home"))
    else:
        try:
            room.delete()
            messages.success(request, "Delete room completely.")
            return redirect(reverse("users:profile", kwargs={"pk": room_host.pk}))
        except Exception as e:
            print(e)
            messages.error(request, "Something wrong while deleting room. 😥")
            return redirect(reverse("users:profile", kwargs={"pk": room_host.pk}))
