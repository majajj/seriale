from django.urls import path

from .views import \
    search_show, \
    search_actor_from_show

urlpatterns = [
    path('shows/', search_show),
    path('<str:title_id>/actors', search_actor_from_show)
    
]


