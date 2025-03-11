from django.contrib import admin
from .models import Account
from django.contrib.auth.models import User

class AccountAdmin(admin.ModelAdmin):
    filter_horizontal = ('purchased_books',)

admin.site.unregister(User)
admin.site.register(User)
admin.site.register(Account, AccountAdmin)