from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Webtoon, Episode

def index(request):
    """웹툰 목록을 보여준다"""
    try:
        search_webtoon = request.GET['search_webtoon']
    except Exception as e:
        search_webtoon = None

    if search_webtoon:
        toons = Webtoon.objects.filter(title__contains = search_webtoon)
    else:
        toons = Webtoon.objects.all()

    context = {
        'toons': toons,
        'search_webtoon': search_webtoon,
    }
    return render(request, 'webtoon/index.html', context)


def episode_list(request, webtoon_id):
    """웹툰의 에피소드 목록을 보여준다"""
    toon = Webtoon.objects.filter(pk=webtoon_id)
    ep = Episode.objects.filter(webtoon=webtoon_id)
    if not toon.exists() or not ep.exists():
        return redirect('webtoon:index')

    context = {
        'webtoon': toon.get(),
        'ep': ep,
    }
    return render(request, 'webtoon/episode_list.html', context)
