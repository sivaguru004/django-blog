from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')
    search_fields = ('title', 'content')
    list_filter = ['catagory', 'created_at']

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Catagory)
admin.site.register(AboutUs)