from django.shortcuts import render, get_object_or_404
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


# Submit Comment Form View
def book_details(request, slug):
   queryset = BookStorePage.objects.filter(status=1)
   context_object_name = 'book_list'
   book_details_list = get_object_or_404(queryset, slug=slug)
   template_name = "store/bookpage.html"
   paginate_by = 6

   return render(
      request,
      "store/bookpage.html",
      {"book": book_details_list,
      },  
   )