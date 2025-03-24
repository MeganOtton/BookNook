from django.core.management.base import BaseCommand
from profile.models import Profile
from Store.models import BookStorePage
from profile.tasks import perform_additional_tasks
from django.utils import timezone

class Command(BaseCommand):
    help = 'Checks and updates user roles based on age and updates visible books'

    def handle(self, *args, **options):
        for profile in Profile.objects.all():
            Profile.update_visible_books(profile)
        self.stdout.write(self.style.SUCCESS('Successfully checked and updated user roles and visible books'))