from falcon import HTTPInternalServerError, HTTPBadRequest, HTTP_201
from sqlalchemy.exc import IntegrityError

from app.models import Video
from app.log import get_logger

LOG = get_logger()


class VideoResource:

    def on_get(self, req, resp):
        session = req.context.session
        page = req.get_param_as_int('page', default=0)
        limit = req.get_param_as_int('limit', default=0)
        if page < 0 or limit < 0:
            raise HTTPBadRequest(title='Invalid Pagination',
                                 description='Pagination cannot be negative ')

        if page == 0 or limit == 0:
            offset = 0
        else:
            offset = ((page - 1) * limit)
        if limit and offset:
            videos = session.query(Video).order_by(Video.published_on.desc()).offset(offset).limit(limit).all()
        else:
            videos = session.query(Video).order_by(Video.published_on.desc()).all()
        result = []
        for video in videos:
            result.append(video.todict())

        req.context.result = result


class VideoSearchResource:
    def on_get(self, req, resp):
        session = req.context.session
        page = req.get_param_as_int('page', default=0)
        limit = req.get_param_as_int('limit', default=0)
        title = req.get_param('title')
        description = req.get_param('description')
        if page < 0 or limit < 0:
            raise HTTPBadRequest(title='Invalid Pagination',
                                 description='Pagination cannot be negative ')

        if page == 0 or limit == 0:
            offset = 0
        else:
            offset = ((page - 1) * limit)

        if title or description:
            videos = Video.apply_similarity(session, title, description)
        else:
            raise HTTPBadRequest(title='Bad Request',
                                 description='Please provide title or description')

        result = []
        LOG.info(videos)
        for video in videos:
            result.append(video[0].get_minified_json_dict())

        req.context.result = result

