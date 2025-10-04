from django.urls import path
from .views import movie_details
from .views import episode_details
from .views import genre
from .views import health_check
from .views import recommend_movies

urlpatterns = [
    path("movie/", movie_details, name="Movie Details"),
    path('episode/', episode_details, name='Episode Details'),
    path('genre/',genre, name='Top 15 in Genre'),
    path('health/',health_check,name='Health Check'),
    path("recommendations/", recommend_movies, name="Movie Recommendations"),
]
