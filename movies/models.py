from django.db import models
# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=150)
    overview = models.TextField(max_length=300)
    poster = models.ImageField(null=True)
    producer = models.ManyToManyField("Producer", verbose_name="producer_movie")
    distributor = models.ManyToManyField("Distributor", verbose_name="distributor_movie")
    actor = models.ManyToManyField("Actor", verbose_name="actor_movie")
    genre = models.ManyToManyField("Genre", verbose_name="genre_movie")
    snapshot = models.ManyToManyField("Snapshot", verbose_name="snapshot_movie")

    def __str__(self):
        return self.title
    
class Producer(models.Model):
    producer = models.CharField(max_length=150)
    
    def __str__(self):
        return self.producer
    
class Distributor(models.Model):
    distributor = models.CharField(primary_key=True, max_length=150)

    def __str__(self):
        return self.distributor
    
class Actor(models.Model):
    actor = models.CharField(max_length=50)

    def __str__(self):
        return self.actor
    
class Country(models.Model):
    country = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return self.country
    
class Genre(models.Model):
    genre = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return self.genre
    
class Snapshot(models.Model):
    snapshot = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)