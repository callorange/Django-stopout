from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:webtoon_id>/', views.episode_list, name='episode_list'),
]
