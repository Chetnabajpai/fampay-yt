import requests

from app.config import YT_SEARCH_LINK
from app.log import get_logger

LOG = get_logger()


def get_video_list_from_youtube(search_string, api_key):

    next_page_token = ''
    response = None
    final_videos = []
    try:
        response = requests.get(YT_SEARCH_LINK,
                                params={
                                    "part": 'snippet',
                                    "maxResults": 50,
                                    "q": search_string,
                                    "key": api_key,
                                    "pageToken": next_page_token,
                                    "publishedAfter": '2020-01-01'
                                })
    except Exception as ex:
        LOG.error("Error running Youtube API, %s", ex)
    return response
