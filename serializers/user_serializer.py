"""
    Description: 用户api参数的序列化模型
    :author: zouzhisheng
    :copyright: (c) 2021, Tungee
    :date created: 2021-06-03
    :python version: 3.5
"""
import werkzeug
from flask_restplus import reqparse, fields, inputs
from api import api, basic_serialization


user_fields = api.model("UserFields", {
    'id': fields.String(),
    'nick_name': fields.String(),
    'real_name': fields.String(),
    'phone': fields.String(),
    'avatar': fields.String(),
    'role_type': fields.Integer()
})


class SignUpSerializer(object):
    @property
    def post_request_parser(self):
        request_parser = reqparse.RequestParser()
        request_parser.add_argument('nick_name', type=str, required=True, trim=True, location='form', help='用户昵称')
        request_parser.add_argument('real_name', type=str, required=True, location='form', help='用户姓名')
        request_parser.add_argument('phone', type=inputs.regex(r'^(13\d|14[5|7]|15\d|166|17'
                                                               r'[3|6|7]|18\d)\d{8}$'),
                                    required=True, trim=True, location='form', help="手机号码")
        request_parser.add_argument('password', type=str, required=True, trim=True, location='form', help='密码')
        request_parser.add_argument('confirm_password', type=str, required=True, trim=True, location='form',
                                    help='确认密码')

        return request_parser


class LoginSerializer(object):
    @property
    def post_request_parser(self):
        request_parser = reqparse.RequestParser()
        request_parser.add_argument('phone', type=str, required=True, location='form',
                                    help='电话号码', default='13247662414')
        request_parser.add_argument('password', type=str, required=True, location='form',
                                    help='用户密码', default='123456')
        return request_parser

    @property
    def post_response_parser(self):
        # 继承公用的返回数据结构
        response_parser = api.clone('User', basic_serialization, {
            "data": fields.Nested(user_fields)
        })

        return response_parser


class UserAvatarSerializer(object):
    @property
    def post_request_parser(self):
        request_parser = reqparse.RequestParser()
        request_parser.add_argument('avatar', type=werkzeug.datastructures.FileStorage,
                                    required=True, trim=True, location='files', help='用户头像')
        return request_parser

    @property
    def post_response_parser(self):
        response_parser = api.clone("Avatar", basic_serialization, {
            'data': fields.String()
        })
        return response_parser


class UsersSerializer(object):
    @property
    def get_request_parser(self):
        request_parser = reqparse.RequestParser()
        request_parser.add_argument('user_id', required=False, type=str, location='args', help='用户ID')
        request_parser.add_argument('page', required=False, type=int, location='args', default=0)
        request_parser.add_argument('page_size', required=False, type=int, location='args', default=10)
        return request_parser

    @property
    def response_parser(self):
        new_user_fields = api.clone('new_user_fields', user_fields, {
            'role_type_name': fields.String
        })
        response_parser = api.clone('User', basic_serialization, {
            "data": fields.List(fields.Nested(new_user_fields))
        })

        return response_parser

    @property
    def put_request_parser(self):
        request_parser = reqparse.RequestParser()
        request_parser.add_argument('user_id', type=str, required=True, location='form')
        request_parser.add_argument('nick_name', type=str, required=True, trim=True, location='form')
        request_parser.add_argument('real_name', type=str, required=True, location='form')
        request_parser.add_argument('phone', type=inputs.regex(r'^(13\d|14[5|7]|15\d|166|17'
                                                               r'[3|6|7]|18\d)\d{8}$'),
                                    required=True, trim=True, location='form')
        return request_parser

    @property
    def post_request_parser(self):
        request_parser = SignUpSerializer().post_request_parser.copy()
        request_parser.remove_argument("confirm_password")
        request_parser.add_argument("role_type", type=int, required=True, location='form', default=0)
        return request_parser
