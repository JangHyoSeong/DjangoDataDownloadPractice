from django.db import models
# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=150)
    overview = models.TextField(max_length=300)
    poster = models.ImageField()
    producer = models.ManyToManyField("Producer", verbose_name="producer_movie")
    
    def __str__(self):
        return self.title
    
class Producer(models.Model):
    producer = models.CharField(max_length=150)
    
    def __str__(self):
        return self.producer