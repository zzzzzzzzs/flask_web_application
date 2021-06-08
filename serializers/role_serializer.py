"""
    Description: role_api参数序列化模型
    :author: zouzhisheng
    :copyright: (c) 2021, Tungee
    :date created: 2021-06-08
    :python version: 3.5
"""
from flask_restplus import fields
from api import api, basic_serialization

permission_fields = api.model("PermissionFields", {
    'name': fields.String(),
    'action': fields.String()
})

role_fields = api.model("RoleFields", {
    'name': fields.String(),
    'role_type': fields.Integer(),
    'operation_permissions': fields.List(fields.Nested(permission_fields))
})


class RoleSerializer(object):

    @property
    def get_response_parser(self):

        response_parser = api.clone('Role', basic_serialization, {
            'data': fields.List(fields.Nested(role_fields))
        })
        return response_parser

