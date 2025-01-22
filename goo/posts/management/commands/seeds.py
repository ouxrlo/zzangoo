from django.core.management.base import BaseCommand
from zzangoo.goo.posts.management.commands.seeds import run_seed
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Generates seed data for posts"

    def handle(self, *args, **kwargs):
        run_seed()
