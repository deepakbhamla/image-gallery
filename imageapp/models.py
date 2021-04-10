from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image


class Tag(models.Model):
    tag_name = models.CharField(max_length=99)
    slug = models.CharField(max_length=130)

    class Meta:
        verbose_name_plural = "Tag"


    def __str__(self):
        return self.tag_name


class Gallery(models.Model):
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to = 'media/')


 

    