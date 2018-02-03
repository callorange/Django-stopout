# Django-stopout

패스트캠퍼스 웹개발 과정 [스탑아웃 과제](https://github.com/Fastcampus-WPS-7th/Tips/blob/master/stopout.md)

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