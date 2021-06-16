from django.http.request import HttpHeaders, HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseBase, HttpResponseGone, HttpResponseRedirect
import requests
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .config import shows_url, actors_url, actors_ending_url

# Create your views here.

def execute_search_show():
    """komentarz"""

    url = shows_url

    return requests.get(url=url, timeout=5)

def execute_actors_search(title_id):

    url = actors_url + title_id + actors_ending_url

    return requests.get(url=url, timeout=5)


@api_view(['GET'])
def search_show(request):
    """komentarz"""

    result = {
        "status": None,
        "message": None,
    }

    shows = execute_search_show()

    result["message"] = "There was a problem with send request"
    result["status"] = shows.status_code

    try:
        if shows.status_code in [200, 201, 202]:
            shows = shows.json()
            length = len(shows)
            list_of_shows = []

            for show in shows:

                show_id = show["_embedded"]["show"]["id"]
                show_title = show["_embedded"]["show"]["name"]
                list_of_shows.append({"id": show_id, "title": show_title})


            return render(request, "shows/index.html", {
                "shows": list_of_shows
            })
    except:
        return Response(result)

@api_view(['GET'])
def search_actor_from_show(request, title_id):
    """komentarz"""

    result = {
        "status": None,
        "message": None,
    }

    actors = execute_actors_search(title_id=title_id)

    result["message"] = "There was a problem with send request"
    result["status"] = actors.status_code

    if actors.status_code in [200, 201, 202]:
        actors = actors.json()
    
    return Response(actors)
