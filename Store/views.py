from django.shortcuts import render
from django.views import generic
from .models import BookStorePage

# Create your views here.
class BookList(generic.ListView):
   queryset = BookStorePage.objects.filter(status=1)
   context_object_name = 'book_list'
   template_name = "store/index.html"
   paginate_by = 6

def Store(request):
    return render(request, 'store/index.html')