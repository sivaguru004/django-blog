from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

#catagory
class Catagory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    img_url = models.ImageField(null=True, blank=True, upload_to='posts/images')
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.img_url:
            self.img_url = 'https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg'
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def formatted_imag_url(self):
        url = self.img_url if self.img_url.__str__().startswith(('http://','https://')) else self.img_url.url
        return url

    def __str__(self):
        return self.title

class AboutUs(models.Model):
    content = models.TextField()