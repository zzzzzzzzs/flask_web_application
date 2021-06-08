"""
    Description: 权限相关的视图
    :author: zouzhisheng
    :copyright: (c) 2021, Tungee
    :date created: 2021-06-08
    :python version: 3.5
"""
from flask_restplus import Resource, abort
from flask_login import login_required, logout_user, current_user
from api import api


ns = api.namespace('permission', description='Permission operations')


# @ns.route('/permission/')
# class Permission(Resource):
#
#     def get(self):
#         """获取对应角色可以看到的权限"""
#         pass