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