from django.conf import settings
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save 
from django.utils.text import slugify
from django.utils import timezone
# Create your models here.


class PostManager(models.Manager):
    def draft(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=True).filter(publish__gte=timezone.now())

    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

class Post(models.Model):
    user         = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    title        = models.CharField(max_length=120)
    image        = models.ImageField(upload_to="images/", null=True, blank=True, height_field="height_field", width_field="width_field")
    height_field = models.IntegerField(default=0)
    width_field  = models.IntegerField(default=0)
    content      = models.TextField()
    draft        = models.BooleanField(default=False)
    publish      = models.DateField(auto_now=False, auto_now_add=False)
    updated      = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp    = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:posts_detail', kwargs={'id':self.id})


    class Meta:
        ordering = ['-timestamp', '-updated']
