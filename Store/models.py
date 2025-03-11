from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator

STATUS = ((0, "Draft"), (1, "Published"))

class Topic(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

# Create your models here.
class BookStorePage(models.Model):
    
    booktitle = models.CharField(max_length=200, unique=True)
    
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.booktitle
        super().save(*args, **kwargs)

    authorname = models.CharField(max_length=200, null=True, blank=True, default='')
    
    genre = models.CharField(max_length=200, null=True, blank=True, default='')

    chapter = models.IntegerField(default=0)

    bookcover = CloudinaryField('image', default='placeholder')

    bookdescription = models.TextField()

    bookprice = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    bookrating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

    topics = models.ManyToManyField('Topic', related_name='books', blank=True)

    # series = models.ManyToManyField('Series', related_name='books')

    # author = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name="blog_posts"
    # )

    status = models.IntegerField(choices=STATUS, default=0)


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

