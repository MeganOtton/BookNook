from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.utils import timezone


STATUS = ((0, "Draft"), (1, "Published"))

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        # Capitalize the first letter of the genre name
        self.name = self.name.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name  # To display the readable name

class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        # Capitalize the first letter of the genre name
        self.name = self.name.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name  # To display the readable name

# Create your models here.
class BookStorePage(models.Model):
    
    booktitle = models.CharField(max_length=200, unique=True, verbose_name="Book Title")
    
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="SYSTEM, DO NOT EDIT")

    authorname = models.CharField(max_length=200, null=True, blank=True, default='', verbose_name="Author Name")
    
    genre = models.ManyToManyField(Genre, related_name='books', blank=True, verbose_name="Genre")

    age_restriction = models.BooleanField(
        choices=[(True, 'Yes'), (False, 'No')],
        default=False,
        verbose_name="Age Restriction (18+)"
    )

    chapter = models.IntegerField(default=0, verbose_name="Amount Of Chapters")

    bookcover = CloudinaryField('image', default='placeholder')

    bookdescription = models.TextField(verbose_name="Book Description")

    bookprice = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, verbose_name="Book Price")

    topics = models.ManyToManyField(Topic, related_name='books', blank=True, verbose_name="Topics")

    # series = models.ManyToManyField('Series', related_name='books')

    # author = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name="blog_posts"
    # )

    created_on = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(choices=STATUS, default=0)
    updated_on = models.DateTimeField(auto_now=True)

    def is_hidden_by_user(self, user):
        return user.profile.hidden_books.filter(id=self.id).exists()

    @property
    def average_rating(self):
        avg = self.comments.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0.0

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.booktitle
        super().save(*args, **kwargs)

    def __str__(self):
         return f"{self.booktitle} Author {self.authorname}"

    class Meta:
        ordering = ["-created_on"]

class Comment(models.Model):
    bookstorepage = models.ForeignKey(BookStorePage, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    title = models.CharField(max_length=200)
    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Book Rating")
    body = models.TextField()
    approved = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment by {self.author} on {self.bookstorepage}, | {self.body}"
    
