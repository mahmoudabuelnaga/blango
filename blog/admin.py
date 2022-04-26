from django.contrib import admin
from blog.models import Tag, Post, Comment, AuthorProfile

# Register your models here.

class PostAdmin(admin.ModelAdmin):
  list_display = ['slug','published_at']
  prepopulated_fields = {"slug":("title",)}

admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(AuthorProfile)