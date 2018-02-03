from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'webtoon/index.html')


def episode_list(request, webtoon_id):
    return render(request, 'webtoon/episode_list.html')
