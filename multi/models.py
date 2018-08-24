from django.db import models


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    content = models.TextField()
    published = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
