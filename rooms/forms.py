from django import forms
from django_countries.fields import CountryField
from . import models


class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere", required=False)
    country = CountryField(default="KR").formfield(required=False)
    room_type = forms.ModelChoiceField(
        empty_label="Any kind", required=False, queryset=models.RoomType.objects.all()
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    facilities = forms.ModelMultipleChoiceField(
        queryset=models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    house_rules = forms.ModelMultipleChoiceField(
        queryset=models.HouseRule.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )


class EditRoomForm(forms.Form):

    name = forms.CharField(widget=forms.TextInput(attrs={"class": "custom_input"}))
    description = forms.CharField(
        widget=forms.Textarea(attrs={"style": "resize:none", "class": "custom_input"})
    )
    country = CountryField().formfield(
        widget=forms.Select(attrs={"class": "custom_input"})
    )
    city = forms.CharField(widget=forms.TextInput(attrs={"class": "custom_input"}))
    price = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "custom_input"})
    )
    address = forms.CharField(widget=forms.TextInput(attrs={"class": "custom_input"}))
    guests = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "custom_input"})
    )
    beds = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "custom_input"}))
    bedrooms = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "custom_input"})
    )
    baths = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "custom_input"})
    )
    check_in = forms.TimeField(widget=forms.TimeInput(attrs={"class": "custom_input"}))
    check_out = forms.TimeField(widget=forms.TimeInput(attrs={"class": "custom_input"}))
    instant_book = forms.BooleanField(required=False)
    room_type = forms.ModelChoiceField(
        queryset=models.RoomType.objects.all(),
        widget=forms.Select(attrs={"class": "custom_input"}),
    )
    amenity = forms.ModelMultipleChoiceField(
        queryset=models.Amenity.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "custom_input"}),
    )
    facility = forms.ModelMultipleChoiceField(
        queryset=models.Facility.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "custom_input"}),
    )
    house_rules = forms.ModelMultipleChoiceField(
        queryset=models.HouseRule.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "custom_input"}),
    )


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = (
            "name",
            "description",
            "country",
            "city",
            "price",
            "address",
            "guests",
            "beds",
            "bedrooms",
            "baths",
            "check_in",
            "check_out",
            "room_type",
            "instant_book",
            "amenity",
            "facility",
            "house_rules",
        )

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "custom_input", "placeholder": "Room Name"}
            ),
            "description": forms.TextInput(
                attrs={"class": "custom_input", "placeholder": "Room Description"}
            ),
            "country": forms.Select(attrs={"class": "custom_input"}),
            "city": forms.TextInput(
                attrs={"class": "custom_input", "placeholder": "City"}
            ),
            "price": forms.NumberInput(
                attrs={"class": "custom_input", "placeholder": "Price"}
            ),
            "address": forms.TextInput(
                attrs={"class": "custom_input", "placeholder": "Address"}
            ),
            "guests": forms.NumberInput(
                attrs={"class": "custom_input", "placeholder": "Guests"}
            ),
            "beds": forms.NumberInput(
                attrs={"class": "custom_input", "placeholder": "Beds"}
            ),
            "bedrooms": forms.NumberInput(
                attrs={"class": "custom_input", "placeholder": "Bedrooms"}
            ),
            "baths": forms.NumberInput(
                attrs={"class": "custom_input", "placeholder": "Baths"}
            ),
            "check_in": forms.TimeInput(
                attrs={"class": "custom_input", "placeholder": "Check_In"}
            ),
            "check_out": forms.TimeInput(
                attrs={"class": "custom_input", "placeholder": "Check_Out"}
            ),
            "room_type": forms.Select(attrs={"class": "custom_input"}),
            "amenity": forms.SelectMultiple(attrs={"class": "custom_input"}),
            "facility": forms.SelectMultiple(attrs={"class": "custom_input"}),
            "house_rules": forms.SelectMultiple(attrs={"class": "custom_input"}),
        }
