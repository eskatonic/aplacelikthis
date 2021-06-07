from aplacelikethis_django.settings import AUTH_PASSWORD_VALIDATORS
from django.db import models
from django.utils import timezone
# User model from Django authentication system. No need to create another User model!
from django.contrib.auth.models import User
# reverse allows you to build URLs by their name and pass optional parameters
from django.urls import reverse

# objects is the default model manager, but you can add additional ones. PublishedManager
# filters only published posts.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    # unique_for_date just makes sure each slug is unique on a given date
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    # auto_now_add adds the date automatically.
    created = models.DateTimeField(auto_now_add=True)
    # auto_now updates the date when you save.
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')
    # Need to add objects here to keep it as the default
    objects = models.Manager()  # Default model manager
    published = PublishedManager()  # Published model manager

    # Meta contains metadata, used here for sorting posts by published date in
    # descending order ('-publish')
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    # Returns 'Canonical" (aka Preferred) URL
    # Use get_absolute_url in templates to link to specific posts
    def get_absolute_url(self):
        return reverse('aplacelikethis:post_details',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'