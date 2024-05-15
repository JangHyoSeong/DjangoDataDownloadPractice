from django.shortcuts import render, redirect
import requests as req
from datetime import datetime
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from .models import *

# Create your views here.

MV_API_KEY = ''
TMDB_API_KEY = ''

def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)

def actor(request):
    actors = Actor.objects.all()
    context = {
        'actors': actors
    }
    return render(request, 'movies/actor.html', context)

def download_movie_list(request):

    MV_URL = f'	http://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?'
    TMDB_URL = f'https://api.themoviedb.org/3/search/movie?'
    
    
    for i in range(40, 50):
        print(i)
        MV_params = {
            'key': MV_API_KEY,
            'curPage': i,
            'itemPerPage': 20,
        }
        
        data = req.get(MV_URL, params=MV_params).json().get('movieListResult').get('movieList')
        
        for movie in data:
            title = movie.get('movieNm')
            movie_code = movie.get('movieCd')
            
            
            TMDB_params = {
                'api_key': TMDB_API_KEY,
                'query': title,
                'language': 'ko-KR',
                'page': 1,
            }
            
            try:
                TMDB = req.get(TMDB_URL, params=TMDB_params).json().get('results')[0]
            except:
                continue
            
            try:
                movie_data = req.get(f'	http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={MV_API_KEY}&movieCd={movie_code}').json().get('movieInfoResult').get('movieInfo')
            except:
                continue
            
            genres = download_genres(movie_data.get('genres'))
            actors = download_actor(movie_data.get('actors'), title)
            countries = download_country(movie_data.get('nations'))
            directors = download_producers(movie_data.get('directors'), title)
            
            overview = TMDB.get('overview')
            poster = TMDB.get('poster_path')
            try:
                opening_date = datetime.strptime(movie_data.get('openDt'), '%Y%m%d').date()
            except:
                opening_date = None
                
            running_time = movie_data.get('showTm')
            if running_time == '':
                running_time = None
            
            movie = Movie(movie_id=movie_code, title=title, overview=overview, opening_date=opening_date, running_time=running_time)
            movie.save()
            
            if poster == '':
                poster_url = ''
            else:
                poster_url = f'https://image.tmdb.org/t/p/original/{poster}'
                download_and_save_image(poster_url, movie, movie_code)
            
            
    print('done')
    
    return redirect('movies:index')

def download_genres(genres):
    
    new_genres = []
    
    if genres == [] or genres is None:
        return list()
    
    for genre in genres:
        new_genre = Genre(genre=genre.get('genreNm'))
        new_genre.save()
        new_genres.append(new_genre)
        
    return new_genres # 리스트 요소를 반환


def download_actor(actors, movie_name):
    
    new_actors = []
    try:
        for idx in range(5):
            actor_name = actors[idx].get('peopleNm')
            URL = 'http://kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?'
            params = {
                'key': MV_API_KEY,
                'peopleNm': actor_name,
                'filmoNames': movie_name,
            }
            actor_data = req.get(URL, params=params).json().get('peopleListResult').get('peopleList')[0]
            actor_name = actor_data.get('peopleNm')
            actor_code = actor_data.get('peopleCd')
            
            TMDB_URL = 'https://api.themoviedb.org/3/search/person?'
            TMDB_params = {
                'api_key': TMDB_API_KEY,
                'query': actor_name,
                'language': 'ko-KR',
            }
            
            new_actor = Actor(actor_code=actor_code, actor=actor_name)
            new_actor.save()
            
            response = req.get(TMDB_URL, params=TMDB_params).json().get('results')
            
            if response != []:
                image_url = f'https://image.tmdb.org/t/p/original/{response[0].get("profile_path")}'
                download_actor_image(image_url, new_actor, actor_code)
            
            new_actors.append(new_actor)
            
    except IndexError:
        return new_actors
    
    return new_actors

def download_country(countries):
    new_countries = []
    
    if countries is None or countries == []:
        return list()
    
    for country in countries:
        country_name = country.get('nationNm')
        new_country = Country(country=country_name)
        new_country.save()
        new_countries.append(new_country)
    
    return new_countries

def download_producers(producers, movie_name):
    
    new_producers = []
    
    if producers == []:
        return list()
    
    for producer in producers:
        URL = 'http://kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?'
        params = {
            'key': MV_API_KEY,
            'peopleNm': producer.get('peopleNm'),
            'filmoNames': movie_name,
        }
        producer_data = req.get(URL, params=params).json().get('peopleListResult').get('peopleList')[0]
        producer_name = producer_data.get('peopleNm')
        producer_code = producer_data.get('peopleCd')
        
        new_producer = Producer(producer_id=producer_code, producer=producer_name)
        new_producer.save()
        new_producers.append(new_producer)
        
    return new_producers

def download_and_save_image(image_url, movie, movie_id):
    response = req.get(image_url)

    if response.status_code == 200:
        img_temp = NamedTemporaryFile()
        img_temp.write(response.content)
        img_temp.flush()
        
        movie.poster.save(f'poster_{movie_id}.jpg', File(img_temp), save=True)
        # img_temp.delete()

def download_actor_image(image_url, actor, actor_id):
    response = req.get(image_url)
    
    if response.status_code == 200:
        img_temp = NamedTemporaryFile()
        img_temp.write(response.content)
        img_temp.flush()
        
        actor.profile_image.save(f'actor_{actor_id}.jpg', File(img_temp), save=True)