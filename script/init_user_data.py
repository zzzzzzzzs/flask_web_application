"""
    Description: 基础数据初始化
    :author: zouzhisheng
    :copyright: (c) 2021, Tungee
    :date created: 2021-06-07
    :python version: 3.5
"""
from app import mongo_db
from model.user import Role, Permission, User
from utils.permission import PERMISSIONS, ROLES


def init_role_and_permission():

    role_type_obj_map = dict()
    super_admin_role = None
    # 初始化角色表
    for role in ROLES:
        role_obj = Role(
            name=role[0],
            role_type=role[1]
        ).save()
        role_type_obj_map[role[1]] = role_obj
        if role[1] == 2:
            super_admin_role = role_obj

    # 初始化权限表
    for permission in PERMISSIONS:
        permission_obj = Permission(
            name=permission[0],
            action=permission[1]
        ).save()

        if permission[2] == 1:
            for _, role in role_type_obj_map.items():
                role.operation_permissions.append(permission_obj.action)
                role.save()
        elif permission[2] == 2:
            role = role_type_obj_map[permission[2]]
            role.operation_permissions.append(permission_obj.action)
            role.save()

    return super_admin_role


def init_super_admin(role):
    User(
        nick_name='super_admin',
        real_name='super_admin',
        phone='13211111111',
        password='123456',
        role_type=role.role_type
    ).save()


if __name__ == '__main__':
    super_role = init_role_and_permission()
    # init_super_admin(super_role)
