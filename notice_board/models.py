from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)

class Ad(models.Model):
    adAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)
    adTitle = models.CharField(max_length=255)
    adText = models.TextField()

class Reply(models.Model):
    replyText = models.TextField()
    replyAd = models.ForeignKey(Ad, on_delete=models.CASCADE)


