from django.shortcuts import render
from django.views import generic


# Create your views here.
class PostList(generic.ListView):
   template_name = "store/index.html"
   paginate_by = 6