from django.contrib import admin
from django.contrib.admin.helpers import ActionForm
from django import forms
from webtoon.models import Webtoon, Episode


class WebtoonPageForm(ActionForm):
    page = forms.IntegerField(required=False)


class WebtoonAdmin(admin.ModelAdmin):

    actions = ['update_webtoon_info', 'update_webtoon_episode']
    action_form = WebtoonPageForm

    def update_webtoon_info(self, request, queryset):
        toon = queryset.get()
        toon.get_webtoon_info()
    update_webtoon_info.short_description = '기본정보 갱신'

    def update_webtoon_episode(self, request, queryset):
        toon = queryset.get()
        if request.POST['page'] != '':
            toon.get_episode_list(int(request.POST['page']))
        else:
            toon.get_episode_list(1)
    update_webtoon_episode.short_description = '에피소드 리스트 갱신(기존정보는 삭제됩니다.)'


admin.site.register(Webtoon, WebtoonAdmin)
admin.site.register(Episode)
