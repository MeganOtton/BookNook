from django.contrib import admin
from .models import BookStorePage, Genre


# Register your models here.
@admin.register(BookStorePage)
class BookStorePageAdmin(admin.ModelAdmin):
    list_display = ('booktitle', 'authorname', 'bookprice', 'bookrating', 'status')
    filter_horizontal = ('genre',)  # Better interface for selecting multiple genres
    search_fields = ('booktitle', 'authorname', 'bookprice', 'bookrating')
    prepopulated_fields = {'slug': ('booktitle',)}
    ordering = ['status' ]

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)