from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('Hello Index')


def episode_list(request, webtoon_id):
    return HttpResponse('Hello List')
