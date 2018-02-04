from django.db import models
from django.utils.dateparse import parse_date

class Webtoon(models.Model):
    webtoon_no = models.IntegerField(default=0)
    title = models.CharField(max_length=200)
    thumbnail = models.CharField(max_length=300) # static 경로로 넣을것.
    author = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    url = models.CharField(max_length=100)

    def get_episode_list(self):
        pass

    def __str__(self):
        return self.title


class Episode(models.Model):
    webtoon = models.ForeignKey(Webtoon, on_delete=models.CASCADE)
    webtoon_no = models.IntegerField(default=0)
    episode_no = models.IntegerField(default=0)
    title = models.CharField(max_length=200, default='')
    thumbnail = models.CharField(max_length=300) # static 경로로 넣을것.
    rating = models.CharField(max_length=4)
    created_date = models.DateField('published date')
    url = models.CharField(max_length=100)

    def __str__(self):
        return "{} - {}".format(self.webtoon, self.title)