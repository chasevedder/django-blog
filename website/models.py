from django.db import models
from customauth.models import MyUser


# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(MyUser)
    content = models.TextField(max_length=10000)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.author.get_full_name() + " - " + self.title


class Comment(models.Model):
    author = models.ForeignKey(MyUser)
    post = models.ForeignKey(BlogPost)
    content = models.TextField(max_length=1000)
    parent = models.ForeignKey('self', null=True, blank=True)

    def __str__(self):
        return self.content
