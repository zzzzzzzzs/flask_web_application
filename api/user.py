"""
    Description: 用户相关视图
    :author: zouzhisheng
    :copyright: (c) 2021, Tungee
    :date created: 2021-06-08
    :python version: 3.5
"""
from flask_restplus import Resource, abort
from flask_login import login_required, logout_user, current_user
from api import api
from logic.user import logic_sign_up, logic_login_in, \
    logic_upload_avatar, logic_query_users, logic_update_user_info, \
    logic_create_user
from serializers.user_serializer import \
    SignUpSerializer, LoginSerializer, UserAvatarSerializer, \
    UsersSerializer
from utils.permission import auth, ADD_USER

# 定义模块的命名空间
ns = api.namespace('user', description='User operations')


@ns.route('/sign-up/')
class SignUp(Resource):
    """用户注册"""
    post_request_parser = SignUpSerializer().post_request_parser

    @ns.expect(post_request_parser, validate=True)
    def post(self):     # pylint: disable=R0201
        """用户注册"""
        # 获取参数并作类型校验，如果校验不通过会立即返回第一个不通过的参数的错误信息给客户端

        args = SignUp.post_request_parser.parse_args()

        ok, status_code, msg = logic_sign_up(args)  # pylint: disable=C0103
        if not ok:
            abort(status_code, msg)
        return msg, status_code


@ns.route('/login/')
class Login(Resource):
    """用户登录视图"""
    post_request_parser = LoginSerializer().post_request_parser
    post_response_parser = LoginSerializer().post_response_parser

    @ns.expect(post_request_parser)
    @ns.marshal_with(post_response_parser, description="返回用户的信息")
    def post(self):     # pylint: disable=R0201
        """用户登录"""

        args = Login.post_request_parser.parse_args()

        ok, status_code, msg = logic_login_in(args)  # pylint: disable=C0103
        if not ok:
            abort(status_code, msg)
        return msg, status_code


@ns.route('/logout/')
class Logout(Resource):
    """用户登出视图"""

    @ns.response(200, 'Logout successfully')
    @login_required
    def post(self):     # pylint: disable=R0201
        """用户登出"""
        logout_user()
        return 'Logout Successfully'


@ns.route('/avatar/')
class UserAvatar(Resource):
    """用户头像视图"""
    post_request_parser = UserAvatarSerializer().post_request_parser
    post_response_parser = UserAvatarSerializer().post_response_parser

    @login_required
    @ns.expect(post_request_parser)
    @ns.marshal_with(post_response_parser, description="返回新的avatar")
    def post(self):
        """上传头像"""
        args = UserAvatar.post_request_parser.parse_args()
        user = current_user
        ok, status_code, msg = logic_upload_avatar(user, args)
        if not ok:
            abort(status_code, msg)
        return msg, status_code


@ns.route('/users/')
class Users(Resource):
    get_request_parser = UsersSerializer().get_request_parser
    put_request_parser = UsersSerializer().put_request_parser
    post_request_parser = UsersSerializer().post_request_parser

    response_parser = UsersSerializer().response_parser

    @login_required
    @ns.expect(get_request_parser, validate=True)
    @ns.marshal_with(response_parser, description="全部/单个用户信息")
    def get(self):
        """获取用户个人信息"""
        args = Users.get_request_parser.parse_args()
        ok, status_code, msg = logic_query_users(args)

        if not ok:
            abort(status_code, msg)

        return msg

    @login_required
    @ns.expect(put_request_parser, validate=True)
    @ns.marshal_with(response_parser, description="修改某用户信息")
    def put(self):
        """修改某个用户信息"""
        args = self.put_request_parser.parse_args()
        ok, status_code, msg = logic_update_user_info(args)
        if not ok:
            abort(status_code, msg)

        return msg

    @login_required
    @auth(ADD_USER)
    @ns.expect(post_request_parser, validate=True)
    @ns.marshal_with(response_parser, description="添加用户")
    def post(self):
        """创建用户"""
        args = self.post_request_parser.parse_args()
        ok, status_code, msg = logic_create_user(args)

        if not ok:
            abort(status_code, msg)

        return msg, status_code
