import redis

from app.celery import wdb_session, celery_app, DBTask
from app.models import Video
from sqlalchemy.exc import IntegrityError
from app.config import REDIS_URL
from app.log import get_logger
from app.services.youtube import get_video_list_from_youtube

LOG = get_logger()
rdb = redis.from_url(REDIS_URL)
YOUTUBE_API_KEY = 'YOUTUBE_API_KEYS'


@celery_app.task(base=DBTask, bind=True, max_retries=2)
def update_db_with_videos(self, search_string):
    # get all cars
    if not rdb.llen(YOUTUBE_API_KEY) > 0:
        LOG.error("All keys expired, please add new keys to redis")

    api_key = rdb.lpop(YOUTUBE_API_KEY)
    LOG.info("$"*100)
    LOG.info(api_key)
    response = get_video_list_from_youtube(search_string, api_key)
    response_json = response.json()
    if response.status_code == 403:
        error_message = response_json['error']['errors'][0]['reason']
        if "quotaExceeded" in error_message.strip():
            rdb.rpush(YOUTUBE_API_KEY, api_key)
            self.retry(countdown=10)
        else:
            LOG.error("HTTP 443 returned - status code = %s, error = %s", response.status_code, response.json())
    elif response.status_code == 200:
        videos = response_json['items']

        if videos:  # if we have gotten the response
            for video in videos:
                result = {
                    'title': video['snippet']['title'],
                    'description': video['snippet']['description'],
                    'url': "https://www.youtube.com/watch?v={}".format(video['id']['videoId']),
                    'thumbnail_url': video['snippet']['thumbnails']['default']['url'],
                    'published_on': video['snippet']['publishedAt']
                }

                new_video_row = Video.add_video(**result)
                wdb_session.add(new_video_row)

                try:
                    LOG.info("All done, now committing a new video to the database...")
                    wdb_session.commit()
                except IntegrityError as ie:
                    LOG.error("Error occurred while adding video, video already exists")
                    pass
                except Exception as ex:
                    LOG.error("Task running failed...")
                    wdb_session.rollback()
        else:
            LOG.error("No data returned from Youtube API...")
    else:
        LOG.error("Unknown response returned - status code = %s, error = %s", response.status_code, response.json())
    try:
        LOG.info("All done, now committing to the database...")
        wdb_session.commit()
        rdb.rpush(YOUTUBE_API_KEY, api_key)
    except Exception as ex:
        LOG.error("Task running failed...")
        wdb_session.rollback()
