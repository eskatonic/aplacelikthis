from typing import List
from django.core import paginator
from django.shortcuts import render, get_object_or_404
# Adding pagination to limit number of posts that appear at once:
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Adding class-based views:
from django.views.generic import ListView
from .models import Post

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'aplacelikethis/post/list.html'

# def post_list(request):
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 5)
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     # posts = Post.published.all()
#     return render(request,
#                   'aplacelikethis/post/list.html',
#                   {'page': page,
#                   'posts': posts})


def post_details(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'aplacelikethis/post/details.html',
                  {'post': post})
