from django.contrib import admin
from .models import BookStorePage


# Register your models here.
@admin.register(BookStorePage)
class BookStorePageAdmin(admin.ModelAdmin):
    list_display = ('booktitle', 'authorname', 'bookprice', 'bookrating', 'status')
    # list_filter = ('status')
    search_fields = ('booktitle', 'authorname', 'bookprice', 'bookrating')
    prepopulated_fields = {'slug': ('booktitle',)}
    ordering = ['status' ]