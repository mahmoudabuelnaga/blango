from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from blog.models import Post
from blog.forms import CommentForm
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
import logging
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from blango_auth.models import User

logger = logging.getLogger(__name__)

# Create your views here.
# from datetime import timedelta

# from django.conf import settings
# from django.utils import timezone

# from blango_auth.models import User
# User.objects.filter(
#     is_active=False,
#     date_joined__lt=timezone.now() - timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
# ).delete()

@cache_page(300)
@vary_on_headers("Cookie")
def index(request):
  from django.http import HttpResponse
  # return HttpResponse(str(request.user).encode("ascii"))
  User.objects.filter(is_active=False, date_joined__lt=timezone.now() - timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)).delete()
  posts = Post.objects.filter(published_at__lte=timezone.now()).select_related("author")
  logger.debug("Got %d posts", len(posts))
  return render(request, "blog/index.html", {'posts':posts})

def post_detail(request, pk=None):
  post = get_object_or_404(Post, pk=pk)
  if request.user.is_active:
    if request.method == 'POST':
      comment_form = CommentForm(request.POST)

      if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.content_object = post
        comment.creator = request.user
        comment.save()
        return redirect(request.path_info)
      
    else:
      comment_form = CommentForm()
  else:
    comment_form = None
  
  return render(request, "blog/post-detail.html", {"post": post, "comment_form": comment_form})

def get_ip(request):
  from django.http import HttpResponse
  print(HttpResponse(request.META['REMOTE_ADDR']))
  return HttpResponse(request.META['REMOTE_ADDR'])
