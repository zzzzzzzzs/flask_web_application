"""
注册路由
"""
from json import dumps
from flask import current_app, make_response
from flask_restplus import Api, fields
from flask_login import LoginManager

api = Api(
    version='1.0',
    title='Flask App demo',
    description='A simple flask application',
    doc='/',  # doc=False
    prefix='/api'
)

login_manager = LoginManager()

basic_serialization = api.model('Basic', {
    'code': fields.Integer(),
    'message': fields.String()
})


# 统一返回接口格式
@api.representation("application/json")
def output_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""
    # 此处为自己添加***************
    rsp = dict()
    if isinstance(data, str):
        rsp['message'] = data
        rsp['code'] = 1
    elif isinstance(data, dict):
        if code not in {200, 201}:
            data = eval(data.pop("message"))
        rsp = data
        rsp['code'] = data.get('code', 1)
        rsp['data'] = data.get('data', list())
        rsp['message'] = data.get('message', 'ok')
        if isinstance(rsp['data'], list):
            rsp['total'] = len(rsp['data'])
    # **************************

    settings = current_app.config.get('RESTFUL_JSON', {})

    # If we're in debug mode, and the indent is not set, we set it to a
    # reasonable value here.  Note that this won't override any existing value
    # that was set.  We also set the "sort_keys" value.
    if current_app.debug:
        settings.setdefault('indent', 4)

    # always end the json dumps with a new line
    # see https://github.com/mitsuhiko/flask/pull/1262
    dumped = dumps(rsp, **settings) + "\n"
    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp


# 路由注册
from api import (
    user,
    role,
    permission
)
