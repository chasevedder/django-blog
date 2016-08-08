from django.db import models
from customauth.models import MyUser

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(MyUser)
    content = models.TextField(max_length=10000)

    def __str__(self):
        return self.author.get_full_name() + " - " + self.title