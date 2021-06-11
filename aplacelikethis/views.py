from typing import List
from django.core import paginator
from django.shortcuts import render, get_object_or_404
# Adding pagination to limit number of posts that appear at once:
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Adding class-based views:
from django.views.generic import ListView
# Adding to allow email:
from django.core.mail import send_mail
# Adding to allow tagging and aggregated counts of tags:
from taggit.models import Tag
from django.db.models import Count

from .forms import EmailPostForm, CommentForm
from .models import Post, Comment

# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 5  # This determines how many posts are going to show at once.
#     template_name = 'aplacelikethis/post/list.html'

def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    # If there's a tag slug, get the Tag object, then filter posts by tag.
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        # __in is a "field lookup"
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    # posts = Post.published.all()
    return render(request,
                  'aplacelikethis/post/list.html',
                  {'page': page,
                  'posts': posts,
                  'tag': tag})


def post_details(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # Retrieve all comments on this post:
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment object (save), but don't save to db yet (commit=False):
            new_comment = comment_form.save(commit=False)
            # Assign current post to comment:
            new_comment.post = post
            # Save new comment to db:
            new_comment.save()
    else:
        # If it's not a POST (i.e., a GET), create a new comment_form:
        comment_form = CommentForm()        

    # Aggregation: Get tags for current post, find posts with the same tag, then order them.
    # flat=True "flattens" the returned results to an array.
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:5]

    return render(request,
                  'aplacelikethis/post/details.html',
                  {'post': post,
                  'comments': comments,
                  'new_comment': new_comment,
                  'comment_form': comment_form,
                  'similar_posts': similar_posts})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if (request.method == 'POST'):
        form = EmailPostForm(request.POST)
        if (form.is_valid()):
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@aplacelikethis.com',
            [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'aplacelikethis/post/share.html',
    {'post': post,
    'form': form,
    'sent': sent})

def portfolio(request):
    return render(request, 'aplacelikethis/portfolio.html')

def about(request):
    return render(request, 'aplacelikethis/about.html')