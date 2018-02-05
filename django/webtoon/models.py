from django.db import models
from .crawler import Webtoon as NaverToon
from django.utils.dateparse import parse_date

import os
from config.settings import BASE_DIR


class Webtoon(models.Model):
    webtoon_no = models.IntegerField(default=0)
    title = models.CharField(max_length=200)
    thumbnail = models.CharField(max_length=300) # static 경로로 넣을것.
    author = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    url = models.CharField(max_length=100)

    def get_webtoon_info(self):
        if self.webtoon_no:
            nt = NaverToon(self.webtoon_no)
            self.webtoon_no = nt.webtoon_id
            self.title = nt.webtoon_title
            # 썸네일은 네이버에서 로딩을 막으므로 로컬에 저장한다.
            thumbnail_dir = os.path.join(os.path.join(BASE_DIR, "static"), 'webtoon_thumb')
            self.thumbnail = 'webtoon_thumb/' + nt.thumbnail_save(thumbnail_dir)[1]
            self.author = nt.webtoon_author
            self.description = nt.webtoon_description
            self.url = nt.webtoon_url
            self.save()

    def get_episode_list(self, page=1):
        nt = NaverToon(self.webtoon_no, page)
        for episode in nt.get_toons()[::-1]:
            thumbnail_dir = os.path.join(os.path.join(BASE_DIR, "static"), 'webtoon_thumb')
            thumbnail_dir = 'webtoon_thumb/' + episode.thumbnail_save(thumbnail_dir)[1]
            ep, created = Episode.objects.get_or_create(
                webtoon=self,
                webtoon_no=episode.webtoon_id,
                episode_no=episode.episode_id,
            )

            if ep.title != episode.title:
                ep.title = episode.title
            if ep.thumbnail != thumbnail_dir:
                ep.thumbnail = thumbnail_dir
            if ep.rating != episode.rating:
                ep.rating = episode.rating
            if ep.created_date != parse_date(episode.created_date.replace('.', '-')):
                ep.created_date = parse_date(episode.created_date.replace('.', '-'))
            if ep.url != episode.episode_url:
                ep.url = episode.episode_url
            ep.save()

    def __str__(self):
        return self.title


class Episode(models.Model):
    webtoon = models.ForeignKey(Webtoon, on_delete=models.CASCADE)
    webtoon_no = models.IntegerField(default=0)
    episode_no = models.IntegerField(default=0)
    title = models.CharField(max_length=200, default='')
    thumbnail = models.CharField(max_length=300) # static 경로로 넣을것.
    rating = models.CharField(max_length=4)
    created_date = models.DateField('date published', null=True)
    url = models.CharField(max_length=100)

    def __str__(self):
        return "{} - {}".format(self.webtoon, self.title)

    class Meta:
        ordering = ['-webtoon_no', '-created_date']
