# Django-stopout

패스트캠퍼스 웹개발 과정 [스탑아웃 과제](https://github.com/Fastcampus-WPS-7th/Tips/blob/master/stopout.md)

## 개발 환경
1. Mac OS X 10.13.3
1. python 3.6.4
1. PyCharm 2017.3.3 (Community Edition)  
Build #PC-173.4301.16, built on January 11, 2018  
JRE: 1.8.0_152-release-1024-b11 x86_64  
JVM: OpenJDK 64-Bit Server VM by JetBrains s.r.o

***

## 1. 네이버 웹툰 크롤러

지정된 웹툰, 페이지의 에피소드 리스트를 출력 할 수 있도록 한다.

1. 각 에피소드의 정보를 담고 있을 EpisodeData 클래스 작성
2. EpisodeData리스트를 반환하는 get_episode_list 함수 작성
3. get_episode_list 함수의 인자는 웹툰 ID, 및 page번호

```python
class EpisodeData:
    """
    하나의 에피소드에 대한 정보를 갖도록 함
    """
    def __init__(self, episode_id, url_thumbnail, title, rating, created_date):
        ...
        
    
def get_episode_list(webtoon_id, page):
    """
    고유ID(URL에서 titleId값)에 해당하는 웹툰의
    특정 page에 있는 에피소드 목록을 리스트로 리턴
    """
```

### 1.1 구현

해당 모듈의 정보는 [위키페이지](https://github.com/callorange/Django-stopout/wiki) 참조.

1. Webtoon 클래스 구현
    - 웹툰 정보를 가짐. (아이디, 제목, 썸네일, 소개, 작가)
    - 현재/이전/다음 페이지 번호를 가짐. (여러페이지 크롤링시 참조)
    - 현재 페이지 에피소드 리스트 갱신여부 Webtoon.page_refreshed로 체크 가능
    - 웹툰 에피소드 데이터 리스트를 가짐. (EpisodeData 클래스)

2. EpisodeData 클래스 구현
    - 웹툰의 각 에피소드에 대한 정보를 가짐. (아이디, 에피소드제목, 썸네일, 평점, 등록일)

3. get_url 함수 구현
    - 지정된 url의 응답 텍스트를 반환하는 함수.
    - method, param 지정가능.

4. get_episode_list 함수 구현
    - 지정된 웹툰 아이디와 페이지번호로 Webtoon 클래스 생성 후 크롤링 작업 진행 후 리스트 반환.



***

## 2. Django - 웹툰 사이트

1. `app` 이름
    - `webtoon`을 사용
    
1. DB 모델
    - `Webtoon` : 웹툰 정보
    - `Episode` : 웹툰 에피소드 정보

2. View
    - 웹툰 목록 및 웹툰의 에피소드 목록 보여주기
    - Url 예시
        - / : 웹툰 목록
        - /웹툰/ : 웹툰 에피소드 목록

3. DB 모델에 크롤링 코드 추가
    - 1번 과제에서 만든 크롤링 코드 활용
    - `Webtoon` 모델에 `Episode`를 자동으로 넣는 로직 구현
 
### 2.1 구현

1. `webtoon` app 추가
1. DB 모델
    - `Webtoon`
        - 웹툰 정보 처리
        - 웹툰 정보 및 에피소드 리스트 갱신
            - `get_webtoon_info`: 웹툰 기본 정보 갱신
            - `get_episode_list`: 에피소드 리스트 갱신( 지정된 페이지 )
    - `Episode`
        - 에피소드 정보 처리
1. View
    - `/`: 웹툰 목록
    - `/<int:webtoon_id>/`: 해당 웹툰의 에피소드 목록(`Paginator` 사용하여 페이징 처리)

1. 크롤링 코드 추가.
    - `admin.py`에 커스텀 액션 구현
    - 커스텀엑션에서 `get_webtoon_info`, `get_episode_list` 함수 호출
    - 썸네일 이미지는 로컬에 저장 후 static url을 db에 저장
        - 경로: `/static/webtoon_thumb/`
        
```python
# admin.py

class WebtoonPageForm(ActionForm):
    page = forms.IntegerField(required=False)


class WebtoonAdmin(admin.ModelAdmin):
    actions = ['update_webtoon_info', 'update_webtoon_episode']
    action_form = WebtoonPageForm
    def update_webtoon_info(self, request, queryset):
        # get_webtoon_info 호출
    update_webtoon_info.short_description = '기본정보 갱신'
    
    def update_webtoon_episode(self, request, queryset):
        # get_episode_list 호출
    update_webtoon_episode.short_description = '에피소드 리스트 갱신'


admin.site.register(Webtoon, WebtoonAdmin)
```
