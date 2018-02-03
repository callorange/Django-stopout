from bs4 import BeautifulSoup


__all__ = [
    'get_episode_list',
]


def get_url_text(url):
    """지정된 url에서 response text를 반환한다."""

class Webtoon:
    """웹툰 정보

    Attributes:
        webtoon_id (int): 웹툰 아이디 기본 0

    Raises:
        ValueError: 웹툰 아이디가 잘 못 지정된 경우 발생
    """

    _webtoon_id = 0
    _current_page = 0

    def __init__(self, webtoon_id=0):
        """웹툰 정보 생성

        네이버에서 기본 정보를 가져와서 추가 한다.

        Args:
            webtoon_id (int): 웹툰 아이디 기본값 0
        """
        if webtoon_id.isnumeric() or webtoon_id < 1:
            raise ValueError('웹툰아이디가 올바르지 않습니다.')
        self._webtoon_id = webtoon_id
        self.info_refresh()

    def info_refresh(self):
        """웹툰 정보를 네이버 웹툰에서 가져온다"""

        #http://comic.naver.com/webtoon/list.nhn?titleId=704595


    @property
    def webtoon_id(self):
        """웹툰 아이디 반환

        Returns:
            int: 웹툰 아이디. 지정되지 않았을 경우 0
        """
        return self._webtoon_id

    @webtoon_id.setter
    def webtoon_id(self, webtoon_id):
        """웹툰 아이디를 설정한다.

        웹툰 아이디가 새로 지정될 경우 가지고 있던 **기존 정보는 초기화** 됩니다.

        Args:
            webtoon_id (int): 새로 지정할 웹툰 아이디

        Raises:
            ValueError: 웹툰 아이디가 0보다 작거나 숫자가 아닐경우
        """
        self._webtoon_id = webtoon_id


class EpisodeData:
    """웹툰의 에피소드 정보"""

    def __init__(self, episode_id, url_thumbnail, title, rating, created_date):
        """웹툰 에피소드 정보 생성

        Args:
            episode_id (int): 에피소드 아이디
            url_thumbnail (str): 에피소드 썸네일 링크
            title (str): 에피소드 정보
            rating (int): 에피소드 평점
            created_date (date): 에피소드 등록일
        """
        self._episode_id = episode_id
        self._url_thumbnail = url_thumbnail
        self._title = title
        self._rating = rating
        self._created_date = created_date

    def __str__(self):
        to_str = "{}화 제목:{}. 별점:{}. 등록일:{}".format(
            self._episode_id,
            self._title,
            self._rating,
            self._created_date,
        )
        return to_str

    @property
    def episode_id(self):
        return self._episode_id

    @property
    def url_thumbnail(self):
        return self._url_thumbnail

    @property
    def title(self):
        return self._title

    @property
    def rating(self):
        return self._rating

    @property
    def created_date(self):
        return self._created_date


def get_episode_list(webtoon_id, page=1):
    """고유ID(URL에서 titleId값)에 해당하는 웹툰의
    특정 page에 있는 에피소드 목록을 리스트로 리턴

    Args:
       webtoon_id (int): 웹툰 아이디
       page (int): 가져올 페이지( 기본값 1 )

    Returns:
        list: EpisodeData 클래스

    Raises:
        ValueError: webtoon_id, page가 잘 못 지정되었을 경우
    """
    pass


if __name__ == '__main__':
    toon = get_episode_list(1111)
    for episode in toon:
        print(episode)
