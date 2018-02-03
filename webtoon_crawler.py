from bs4 import BeautifulSoup


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
        pass


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
