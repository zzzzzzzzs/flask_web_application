"""
    Description: 角色相关视图
    :author: zouzhisheng
    :copyright: (c) 2021, Tungee
    :date created: 2021-06-08
    :python version: 3.5
"""
from flask_restplus import Resource, abort
from flask_login import login_required, current_user
from api import api
from logic.role import logic_get_roles
from serializers.role_serializer import RoleSerializer
from utils.permission import auth, QUERY_PERMISSION

ns = api.namespace('role', description='Role operations')


@ns.route('/roles/')
class Role(Resource):
    get_response_parser = RoleSerializer().get_response_parser

    @login_required
    @auth(QUERY_PERMISSION)
    @ns.marshal_with(get_response_parser, description="用户可以看到的角色列表")
    def get(self):
        """根据用户角色获取他可以看到的角色列表"""
        ok, status_code, msg = logic_get_roles(current_user)
        if not ok:
            abort(status_code, msg)

        return msg, status_code
