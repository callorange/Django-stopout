import re
import requests
from bs4 import BeautifulSoup


__all__ = [
    'get_episode_list',
]


def get_url(url, method='get', url_param=''):
    """지정된 url에서 response text를 반환한다.

    Args:
        url (str): 가져올 url. http:// 혹은 https://로 시작하는 주소여야 합니다.
        method (str): http method. 'get' or 'post'. default 'get'
        url_param (dict): 지정된 url에 같이 보낼 파라미터.

    Returns:
        str: url에서 응답한 response text. 오류 발생시 None을 반환한다.

    Raises:
        ValueError: 인자가 잘못된 경우 발생

    Example:
        >>> get_url('http://comic.naver.com/webtoon/list.nhn','post',url_param={'titleId':704595})
        >>> get_url('http://comic.naver.com/webtoon/list.nhn',url_param={'titleId':704595})
    """
    if url.strip() == '':
        raise ValueError('URL IS BLANK')
    if not(method.lower() in ['get', 'post']):
        raise ValueError('method는 get이나 post여야 합니다.')
    if url_param != '' and not(isinstance(url_param, dict)):
        raise ValueError('url_param은 딕셔너리로 지정해주셔야 합니다.')

    # 일부 웹사이트는 http에서 헤더를 검사해서 응답을 안주는 경우가 있다. (ex: melon.com)
    my_headers = {'user-agent': 'my-app/0.0.1'}

    response = ''
    if method.lower() == 'get':
        response = requests.get(url, params=url_param, headers=my_headers)
    else:
        response = requests.post(url, params=url_param, headers=my_headers)

    if response.status_code != 200:
        return None

    return response.text


class Webtoon:
    """웹툰 정보

    Attributes:
        webtoon_id (int): 웹툰 아이디 기본 0

    Raises:
        ValueError: 웹툰 아이디가 잘 못 지정된 경우 발생
    """
    _webtoon_url = 'http://comic.naver.com/webtoon/list.nhn'

    _webtoon_id = 0
    _webtoon_thumbnail = None
    _webtoon_title = None
    _webtoon_author = None
    _webtoon_description = None

    _page_refreshed = False
    _prev_page = 0
    _current_page = 0
    _next_page = 0

    _episode_list = []

    def __init__(self, webtoon_id=0, page=0):
        """웹툰 정보 생성

        네이버에서 기본 정보를 가져와서 추가 한다.

        Args:
            webtoon_id (int): 웹툰 아이디 기본값 0
        """
        if not(isinstance(webtoon_id, int)) or webtoon_id < 1:
            raise ValueError('웹툰아이디가 올바르지 않습니다.')
        self._webtoon_id = webtoon_id

        if (isinstance(page, int) or page.isnumeric()) and webtoon_id > 0:
            self._current_page = page

    def __str__(self):
        to_str = "웹툰 : {} - {} (작가:{})".format(
            self.webtoon_title,
            self.webtoon_description,
            self.webtoon_author
        )
        return to_str

    def info_refresh(self):
        """웹툰 정보를 네이버 웹툰에서 가져온다

        Returns:
            self: 현재 인스턴스
        """
        naver_page = get_url(self._webtoon_url, url_param={'titleId': self._webtoon_id})

        if naver_page:
            # BeautifulSoup 파싱
            soup_page = BeautifulSoup(naver_page, 'lxml')
            comic_info = soup_page.select_one('.comicinfo')

            if comic_info:
                comic_thumb = comic_info.select_one('div.thumb img')
                comic_title = comic_info.select_one('div.detail h2')
                comic_author = comic_info.select_one('div.detail h2 span')
                comic_desc = comic_info.select_one('div.detail > p')

                if comic_thumb:
                    self._webtoon_thumbnail = comic_thumb['src']
                if comic_title:
                    self._webtoon_title = comic_title.find(text=True, recursive=False).strip()
                if comic_author:
                    self._webtoon_author = comic_author.text.strip()
                if comic_desc:
                    self._webtoon_description = comic_desc.text.strip()

        return self

    def page_refresh(self):
        """현재 페이지의 에피소드 리스트를 갱신한다.

        Returns:
            self: 현재 인스턴스
        """
        if self._current_page < 1:
            raise ValueError("조회할 페이지가 지정되지 않았습니다.")

        # 에피소드 리스트 초기화
        self._episode_list = []

        # 네이버 페이지 조회
        naver_page = get_url(self._webtoon_url, url_param={'titleId': self._webtoon_id, 'page': self._current_page})

        if naver_page:
            # BeautifulSoup 파싱
            soup_page = BeautifulSoup(naver_page, 'lxml')

            # 페이지 정보 뽑기
            page_info = soup_page.select_one('div.paginate .page_wrap')
            if page_info:
                page_prev = page_info.select_one('a.pre')
                page_current = page_info.select_one('strong.page')
                page_next = page_info.select_one('a.next')

                # 지정된 페이지가 실제로 존재하는지 확인. 네이버 웹툰은 페이지 번호가 없어도 마지막 페이지를 리턴한다.
                if page_current and str(self._current_page) == page_current.em.text.strip():
                    if page_prev:
                        self._prev_page = self._current_page - 1
                    if page_next:
                        self._next_page = self._current_page + 1
                    else:
                        self._next_page = self._current_page
                else:
                    self._current_page = 0
                    self._prev_page = 0
                    self._next_page = 0
                    self._page_refreshed = False
                    self._episode_list = []

            # 에피소드 리스트 만들기. 페이지번호 갱신이 정상으로 끝났을때
            if self._current_page > 0:
                episodes = soup_page.select('table.viewList tr')
                for episode in episodes[1:]:
                    item_list = episode.find_all('td')
                    episode_thumbnail = item_list[0].find('img')['src']
                    episode_id = item_list[0].find('a')['href']
                    episode_id = re.search(r"no=(\d+)", episode_id).group(1)
                    episode_title = item_list[1].text.strip()
                    episode_rating = item_list[2].find('strong').text.strip()
                    episode_created_date = item_list[3].text.strip()

                    e = EpisodeData(self._webtoon_id, episode_id, episode_thumbnail, episode_title, episode_rating, episode_created_date)
                    self._episode_list.append(e)

                self._page_refreshed = True

        return self

    def get_toons(self, page=0):
        """현재 페이지의 웹툰 에피소드 목록을 반환한다.

        Args:
            page (int): 가져올 페이지

        Returns:
            list: EpisodeData 클래스 리스트
        """
        if not(isinstance(page, int)) or page > 0:
            self.current_page = page

        if self.page_refreshed:
            return self._episode_list
        else:
            self.page_refresh()
            return self._episode_list

    @property
    def webtoon_url(self):
        """웹툰 웹페이지 url을 반환

        Returns:
            str: 웹툰의 url
        """
        return self._webtoon_url + '?titleId=' + str(self.webtoon_id)

    @property
    def webtoon_id(self):
        """웹툰 아이디 반환

        Returns:
            int: 웹툰 아이디. 지정되지 않았을 경우 0
        """
        return self._webtoon_id

    @property
    def webtoon_thumbnail(self):
        """웹툰 썸네일 경로 반환

        Returns:
            str: 웹툰 썸네일 이미지 경로
        """
        if self._webtoon_thumbnail:
            return self._webtoon_thumbnail
        else:
            self.info_refresh()
            return self._webtoon_thumbnail

    @property
    def webtoon_title(self):
        """웹툰 제목 반환

        Returns:
            str: 웹툰 제목
        """
        if self._webtoon_title:
            return self._webtoon_title
        else:
            self.info_refresh()
            return self._webtoon_title

    @property
    def webtoon_author(self):
        """웹툰 작가명 반환

        Returns:
            str: 웹툰 작가명
        """
        if self._webtoon_author:
            return self._webtoon_author
        else:
            self.info_refresh()
            return self._webtoon_author

    @property
    def webtoon_description(self):
        """웹툰 설명 반환

        Returns:
            str: 웹툰 설명
        """
        if self._webtoon_description:
            return self._webtoon_description
        else:
            self.info_refresh()
            return self._webtoon_description

    @property
    def page_refreshed(self):
        """현재 페이지 갱신여부 반환

        Returns:
            bool: 현재 페이지 갱신여부
        """
        return self._page_refreshed

    @property
    def prev_page(self):
        """이전 페이지 번호 반환

        Returns:
            int: 이전 페이지 번호. 없을경우 0
        """
        return self._prev_page

    @property
    def next_page(self):
        """다음 페이지 번호 반환

        Returns:
            int: 다음 페이지 번호. 현재페이지가 마지막이면 현제페이지와 같음
        """
        return self._next_page

    @property
    def current_page(self):
        """현재 페이지 번호 반환

        Returns:
            int: 현재 페이지 번호. 지정되지 않았을 경우 0
        """
        return self._current_page

    @current_page.setter
    def current_page(self, page):
        """현재 페이지 번호를 세팅한다.

        Args:
            page (int): 새로 지정할 현재 페이지
        """
        if not(isinstance(page, int)) or page > 0:
            self._current_page = page
            self._page_refreshed = False

    @property
    def current_page_url(self):
        """현재 페이지의 웹페이지 url을 반환

        Returns:
            str: 웹툰의 현재 페이지 url
        """
        if self._page_refreshed:
            self.page_refresh()
        return self._webtoon_url + '?titleId=' + str(self.webtoon_id) + '&page=' + str(self.current_page)


class EpisodeData:
    """웹툰의 에피소드 정보"""

    def __init__(self, webtoon_id, episode_id, url_thumbnail, title, rating, created_date):
        """웹툰 에피소드 정보 생성

        Args:
            webtoon_id (int): 웹툰의 아이디
            episode_id (int): 에피소드 아이디
            url_thumbnail (str): 에피소드 썸네일 링크
            title (str): 에피소드 정보
            rating (int): 에피소드 평점
            created_date (date): 에피소드 등록일
        """
        self._webtoon_id = webtoon_id
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
    def episode_url(self):
        """해당 에피소드 url 반환

        Returns:
            str: 해당 에피소드를 볼 수 있는 url주소
        """
        return "http://comic.naver.com/webtoon/detail.nhn?titleId=" + str(self._webtoon_id) + "&no=" + str(self.episode_id)

    @property
    def webtoon_id(self):
        return self._webtoon_id

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
    toon = Webtoon(webtoon_id)
    toon.current_page = page
    return toon.get_toons()


if __name__ == '__main__':
    # a = Webtoon(704595, 1)
    # a = Webtoon(374974, 1)
    # print(a.webtoon_id)
    # print(a.webtoon_title)
    # print(a.webtoon_author)
    # print(a.webtoon_thumbnail)
    # print(a.webtoon_description)
    # a.page_refresh()
    # print(a.current_page)
    # print(a.prev_page)
    # print(a.next_page)

    for episode in get_episode_list(374974):
        print(episode)