from django.contrib import admin
from .models import Post

# admin.site.register(Post)
@admin.register(Post)
# You can change the way Django shows your info in the admin site with ModelAdmin
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    # list_filter creates a filter based on the fields you select
    list_filter = ('status', 'created', 'publish', 'author')
    # search_fields created a search bar that works on whatever fields you select
    search_fields = ('title', 'body')
    # When you create a new post, the slug field gets populated automatically
    prepopulated_fields = {'slug': ('title',)}
    #raw_id_fields lets you look up authors based on id
    raw_id_fields = ('author',)
    # date_hierarchy creates nav links via dates
    date_hierarchy = 'publish'
    # ordering specifies the default sorting criteria
    ordering = ('status', 'publish')