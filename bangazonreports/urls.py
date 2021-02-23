from django.urls import path
from .views import favorited_sellers

urlpatterns = [
    path('reports/favoritesellers', favorited_sellers),
]
