from django.urls import path
from .views import userfavseller_list

urlpatterns = [
    path('reports/userfavorites', userfavseller_list),
]
