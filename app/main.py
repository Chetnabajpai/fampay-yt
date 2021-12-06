import falcon

from functools import partial
import simplejson
import rapidjson

from app.database import db_session, init_session
from app.middleware import JSONMiddleware, SessionMiddleware

from app.resources.___init__ import VideoResource, VideoSearchResource, RootResource
from app.log import get_logger
LOG = get_logger()

init_session()

_loads = partial(rapidjson.loads, datetime_mode=rapidjson.DM_ISO8601)
_dumps = partial(simplejson.dumps, default=lambda d: d.isoformat())

json_handler = falcon.media.JSONHandler(dumps=_dumps, loads=_loads)

extra_handlers = {
    'application/json': json_handler,
    'application/json; charset=UTF-8': json_handler,
}

app = falcon.App(middleware=[
    JSONMiddleware(),
    SessionMiddleware(db_session),
])

app.req_options.media_handlers.update(extra_handlers)
app.resp_options.media_handlers.update(extra_handlers)

app.add_route('/', RootResource())
app.add_route('/videos', VideoResource())
app.add_route('/search-videos', VideoSearchResource())

LOG.info('API server started')
