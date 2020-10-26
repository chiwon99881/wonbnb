from django.db import models
from django_countries.fields import CountryField
from django.urls import reverse
from core import models as core_models
from users import models as user_models

# Create your models here.


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item Model """

    name = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """ RoomType Model Definition """

    class Meta:
        # verbose_name is present "specify word+s" in Admin panel
        verbose_name = "Room Type"
        ordering = ["created"]

    pass


class Amenity(AbstractItem):

    """ Amenity Model Definition """

    class Meta:
        # verbose_name_plural is present "specify word" in Admin panel
        verbose_name_plural = "Amenities"

    pass


class Facility(AbstractItem):

    """ Facility Model Definition """

    class Meta:
        verbose_name_plural = "Facilities"

    pass


class HouseRule(AbstractItem):

    """ HouseRule Model Definition """

    class Meta:
        verbose_name = "House Rule"

    pass


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=100)
    file = models.ImageField(upload_to="room_photos")
    # "Room" mean Room class because Room class is located lower then Photo class
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """ Room Model """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    # related_name mean when user objects get "room_set" change name "room_set" to "rooms"
    host = models.ForeignKey(
        user_models.User, related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        RoomType, related_name="rooms", on_delete=models.SET_NULL, blank=True, null=True
    )
    amenity = models.ManyToManyField(Amenity, related_name="rooms", blank=True)
    facility = models.ManyToManyField(Facility, related_name="rooms", blank=True)
    house_rules = models.ManyToManyField(HouseRule, related_name="rooms", blank=True)

    # present Room Object to name
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    def total_rating_average(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews), 1)
        return 0

    def get_absolute_url(self):
        # return f"/rooms/{self.pk}"
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def first_photo(self):
        (photo,) = self.photos.all()[:1]
        # "photo," means that get first element of array
        # For example, one, two, three = self.photos.all() this means that
        # one is first element, two is second element, three is third element of array
        return photo.file.url

    def get_last_four_photo(self):
        last_four_photo = self.photos.all()[1:5]
        return last_four_photo
