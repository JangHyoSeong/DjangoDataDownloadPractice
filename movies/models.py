from django.db import models
# Create your models here.

class Movie(models.Model):
    movie_id = models.CharField(primary_key=True, max_length=50)
    title = models.CharField(max_length=150)
    overview = models.TextField(max_length=300)
    poster = models.ImageField(blank=True, upload_to='poster/')
    opening_date = models.DateField(null=True)
    running_time = models.IntegerField(null=True)
    producer = models.ManyToManyField("Producer", verbose_name="producer_movie")
    actor = models.ManyToManyField("Actor", verbose_name="actor_movie")
    genre = models.ManyToManyField("Genre", verbose_name="genre_movie")

    def __str__(self):
        return self.title
    
class Producer(models.Model):
    producer_id = models.CharField(primary_key=True, max_length=50)
    producer = models.CharField(max_length=150)
    
    def __str__(self):
        return self.producer
    
class Actor(models.Model):
    actor_code = models.CharField(primary_key=True, max_length=50)
    actor = models.CharField(max_length=50)
    profile_image = models.ImageField(blank=True, upload_to='actor/')

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
    
def snapshot_upload_to(instance, filename):
    return f'{instance.movie.title}/snapshot/{filename}'

class Snapshot(models.Model):
    snapshot = models.ImageField(upload_to=snapshot_upload_to)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='snapshots')
    
    def __str__(self):
        return f'Snapshot for {self.movie.title}'