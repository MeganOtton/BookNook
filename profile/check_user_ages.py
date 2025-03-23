from django.core.management.base import BaseCommand
from profile.models import Profile
from profile.tasks import check_and_update_user_role

class Command(BaseCommand):
    help = 'Checks and updates user roles based on age'

    def handle(self, *args, **options):
        for profile in Profile.objects.all():
            check_and_update_user_role(profile)
        self.stdout.write(self.style.SUCCESS('Successfully checked and updated user roles'))