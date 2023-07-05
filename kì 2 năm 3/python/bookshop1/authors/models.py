from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    birth_year = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name