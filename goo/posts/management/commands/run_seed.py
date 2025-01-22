from django.core.management.base import BaseCommand
from posts.models import Post
from django_seed import Seed
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Seed database with sample data"

    def handle(self, *args, **options):
        seeder = Seed.seeder()

        # Author 필드에 사용자 지정
        author = User.objects.first()  # 기존 사용자 중 첫 번째 사용자 선택
        if not author:
            author = User.objects.create_user(
                username="seeduser", password="password123"
            )  # 사용자 생성

        seeder.add_entity(
            Post,
            10,
            {
                "author": lambda x: author,  # author 필드를 지정된 사용자로 설정
            },
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS("Successfully seeded database"))
