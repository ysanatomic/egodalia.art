from django.db import models
from django.contrib import admin
import os
from ordered_model.models import OrderedModel
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_limits.limiter import Limiter
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

# Create your models here

class Category(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    show = models.BooleanField(default = True)


    def __str__(self):
        return self.name + ', ID: ' + str(self.id)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "categories"
        verbose_name = "category"

def content_file_name_art(instance, filename):
    print(instance)
    print(instance.pk)
    ext = filename.split('.')[-1]
    filename = "{}.{}".format(instance.id, ext)
    return os.path.join('art', filename)

class VisualArt(OrderedModel):
    name = models.CharField(max_length=100)
    art = models.ImageField(upload_to = 'art/')
    thumbnail = models.ImageField(upload_to = 'thumbnails/', blank=True)
    description = models.TextField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    show = models.BooleanField(default = True)
    categories = models.ManyToManyField(Category)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def admin_image(self):
        return '<a href="/art/{}">art/{}</a>'.format(self.id) 


    class Meta:
        ordering = ["order"]
        verbose_name_plural = "arts"
        verbose_name = "art"

@receiver(post_save, sender=VisualArt)
def handleSavedArts(sender, instance, created, **kwargs): # we need this to move the new object always on top in ordering
    if created: # we make sure its created and not updated
        instance.top()

        try:
            f = BytesIO()
            image = Image.open(instance.art.path) 
            MAX_SIZE = (1200, 1200)
            image.thumbnail(MAX_SIZE)

            ext = instance.art.name.split('.')[-1]
            if ext in ['jpg', 'jpeg']:
                ftype = 'JPEG'
            elif ext == 'gif':
                ftype = 'GIF'
            elif ext == 'png':
                ftype = 'PNG'
            else:
                return False
            image.save(f, format=ftype)
            s = f.getvalue()
            instance.thumbnail.save(instance.art.name, ContentFile(s))
        except Exception as e:
            print(e)
        finally:
            f.close()


class Comment(models.Model):
    posted_by = models.CharField(max_length=32)
    comment = models.TextField()
    posted_on = models.DateTimeField(auto_now_add = True)
    visualart = models.ForeignKey(VisualArt, on_delete=models.CASCADE)

class BlogCategory(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    show = models.BooleanField(default = True)


    def __str__(self):
        return self.name + ', ID: ' + str(self.id)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "blog categories"
        verbose_name = "blog category"

class Post(models.Model):
    title = models.CharField(max_length=80)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    category = models.ForeignKey(BlogCategory, verbose_name="Category", on_delete=models.PROTECT, null=True, default=None)
    views = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class AboutMe(models.Model): # this is a de-facto model for simplicity - doesn't have to be a model, I was just lazy and this is the easiest way
    title = models.CharField(max_length=80)
    body = models.TextField()

    def __str__(self):
        return "About Me: %s" % self.title

    class Meta:
        verbose_name_plural = "About Me" # no plural
        verbose_name = "About Me"


class MyLimiter(Limiter):
    rules = {
        AboutMe: [
            {
                'limit': 1,
                'message': "Only one About Me allowed!",
            },
        ]
    }
