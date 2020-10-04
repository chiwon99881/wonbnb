import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from users import models as user_models
from rooms import models as room_models

NAME = "rooms"


class Command(BaseCommand):

    help = f"This command create {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help=f"How many {NAME} do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(1, 350),
                "guests": lambda x: random.randint(1, 15),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )
        created_room = seeder.execute()
        created_clean = flatten(list(created_room.values()))
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        house_rules = room_models.HouseRule.objects.all()
        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            for i in range(3, random.randint(7, 10)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1,31)}.webp",
                )
            for amenity in amenities:
                ran_num = random.randint(0, 45)
                if ran_num % 2 == 0:
                    # The way to add ManyToManyField is add() method.
                    room.amenity.add(amenity)
            for facility in facilities:
                ran_num = random.randint(0, 45)
                if ran_num % 2 == 0:
                    # The way to add ManyToManyField is add() method.
                    room.facility.add(facility)
            for rule in house_rules:
                ran_num = random.randint(0, 45)
                if ran_num % 2 == 0:
                    # The way to add ManyToManyField is add() method.
                    room.house_rules.add(rule)

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created."))
