from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import BookStorePage, Comment
from .forms import CommentForm

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

def comment_edit(request, slug, comment_id):
    """
    view to edit comments
    """
    if request.method == "POST":

        queryset = BookStorePage.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = True
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating comment!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


# Delete comment view
def comment_delete(request, slug, comment_id):
    """
    view to delete comment
    """
    queryset = BookStorePage.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))