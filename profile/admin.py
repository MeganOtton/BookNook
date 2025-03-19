from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User

class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('purchased_books','wishlisted_books', 'hidden_books', 'hidden_topics')

admin.site.unregister(User)
admin.site.register(User)
admin.site.register(Profile, ProfileAdmin)
