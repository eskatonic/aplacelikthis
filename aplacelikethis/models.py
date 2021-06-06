from aplacelikethis_django.settings import AUTH_PASSWORD_VALIDATORS
from django.db import models
from django.utils import timezone
# User model from Django authentication system. No need to create another User model!
from django.contrib.auth.models import User

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    # auto_now_add adds the date automatically.
    created = models.DateTimeField(auto_now_add=True)
    # auto_now updates the date when you save.
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    # Meta contains metadata, used here for sorting posts by published date in
    # descending order ('-publish')
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
