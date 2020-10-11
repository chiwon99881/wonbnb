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
