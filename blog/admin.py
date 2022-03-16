from django.contrib import admin
from blog.models import Tag, Post, Comment

# Register your models here.

class PostAdmin(admin.ModelAdmin):
  list_display = ['slug','published_at']
  prepopulated_fields = {"slug":("title",)}

admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)