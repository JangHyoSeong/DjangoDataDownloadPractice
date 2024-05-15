# Generated by Django 4.2.9 on 2024-05-15 10:18

from django.db import migrations, models
import django.db.models.deletion
import movies.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('actor_code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('actor', models.CharField(max_length=50)),
                ('profile_image', models.ImageField(blank=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('country', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('genre', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('movie_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150)),
                ('overview', models.TextField(max_length=300)),
                ('poster', models.ImageField(blank=True, upload_to='poster/')),
                ('opening_date', models.DateField(null=True)),
                ('running_time', models.IntegerField()),
                ('actor', models.ManyToManyField(to='movies.actor', verbose_name='actor_movie')),
                ('genre', models.ManyToManyField(to='movies.genre', verbose_name='genre_movie')),
            ],
        ),
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('producer_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('producer', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Snapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('snapshot', models.ImageField(upload_to=movies.models.snapshot_upload_to)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snapshots', to='movies.movie')),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='producer',
            field=models.ManyToManyField(to='movies.producer', verbose_name='producer_movie'),
        ),
    ]
