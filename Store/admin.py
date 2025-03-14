from django.contrib import admin
from .models import BookStorePage, Genre, Topic, Comment


# Register your models here.
@admin.register(BookStorePage)
class BookStorePageAdmin(admin.ModelAdmin):
    list_display = ('booktitle', 'authorname', 'bookprice', 'status')
    filter_horizontal = ('genre','topics')  # Better interface for selecting multiple genres
    search_fields = ('booktitle', 'authorname', 'bookprice')
    prepopulated_fields = {'slug': ('booktitle',)}
    ordering = ['status' ]

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Topic)
class TopicsAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Register your models here.
admin.site.register(Comment)