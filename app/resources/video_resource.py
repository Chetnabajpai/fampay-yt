from apiclient.discovery import build
from app.config import YOUTUBE_API_KEY

from app.log import get_logger

LOG = get_logger()

GOOGLE_APPLICATION_CREDENTIALS = 'credentials.json'

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"


def fetch_videos_from_youtube():

    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    videos = []
    final_videos = []

    next_page_token = None

    try:
        while True:
            res = youtube.search().list(q='heli',
                                        part='snippet',
                                        maxResults=10,
                                        type='video',
                                        pageToken=next_page_token).execute()

            videos += res['items']
            next_page_token = res.get('nextPageToken', None)

            if not next_page_token:
                break

        if videos:  # if we have gotten the response
            for video in videos:
                LOG.info("_"*100)
                LOG.info(video)
                LOG.info("_"*100)

                result = {
                    'title': video['snippet']['title'],
                    'description': video['snippet']['description'],
                    'type': 'video',
                    'url': "https://www.youtube.com/watch?v={}".format(video['snippet']['resourceId']['videoId']),
                    'image_url': video['snippet']['thumbnails']['standard']['url'],
                    'date': video['snippet']['publishedAt']
                }

                final_videos.append(result)
        else:
            LOG.error("No data returned from Youtube API...")

    except Exception as ex:
        LOG.warning("Youtube API failed %s", ex)

    return final_videos
    # might return empty list, taken care of in caller function


if __name__ == '__main__':
    a = fetch_videos_from_youtube()
    print(a)
