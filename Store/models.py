from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator

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

    bookrating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], verbose_name="Book Rating")

    topics = models.ManyToManyField(Topic, related_name='books', blank=True, verbose_name="Topics")

    # series = models.ManyToManyField('Series', related_name='books')

    # author = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name="blog_posts"
    # )

    status = models.IntegerField(choices=STATUS, default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.booktitle
        super().save(*args, **kwargs)

    def __str__(self):
        return self.booktitle


# class Post(models.Model):
#     title = models.CharField(max_length=200, unique=True)
#     slug = models.SlugField(max_length=200, unique=True)
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="blog_posts"
#     )
#     featured_image = CloudinaryField('image', default='placeholder')
#     content = models.TextField()
#     created_on = models.DateTimeField(auto_now_add=True)
#     status = models.IntegerField(choices=STATUS, default=0)

