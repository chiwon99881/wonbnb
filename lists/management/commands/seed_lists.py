import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models

NAME = "lists"


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
        all_rooms = room_models.Room.objects.all()
        all_users = user_models.User.objects.all()
        seeder.add_entity(
            list_models.List,
            number,
            {
                "name": lambda x: seeder.faker.text(max_nb_chars=15),
                # random.choice is select element one of the list
                "user": lambda x: random.choice(all_users),
            },
        )
        created_pk_list = seeder.execute()
        clean_pk_list = flatten(list(created_pk_list.values()))
        for pk in clean_pk_list:
            list_record = list_models.List.objects.get(pk=pk)
            to_add_rooms = all_rooms[
                random.randint(0, 5) : random.randint(6, 30)  # noqa: E203
            ]
            # "*to_add_rooms" means not just list but all element of the list.
            list_record.rooms.add(*to_add_rooms)
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created."))
