"""
用户相关模型
"""
from datetime import datetime

from flask_login import UserMixin   # 使用flask_login，你的User类须继承UserMixin
from model import mongo_db
from api import login_manager
from configs import config_obj


ROLE_TYPE = (
    (0, "用户"),
    (1, "管理员"),
    (2, "超级管理员")
)


class User(UserMixin, mongo_db.DynamicDocument):
    """
    用户模型
    """
    nick_name = mongo_db.StringField(required=True, max_length=30)
    real_name = mongo_db.StringField(required=True, max_length=30)
    phone = mongo_db.StringField(required=True, min_length=6, max_length=11, unique=True)
    password = mongo_db.StringField(required=True, min_length=6, max_length=30)
    avatar = mongo_db.StringField(default=config_obj['project']['avatar_default_url'])
    role_type = mongo_db.IntField(default=0, choices=ROLE_TYPE)
    is_deleted = mongo_db.BooleanField(default=False)

    meta = {
        'indexes': [
            'phone'
        ]
    }

    def password_is_correct(self, password):
        """
        重写UserMixin方法
        :param password: string
        :return: bool
        """
        if self.password != password:
            return False
        return True


@login_manager.user_loader
def load_user(user_id):
    """
    加载用户
    :param user_id: 用户id
    :return: User object
    """
    return User.objects(pk=user_id).first()


class Role(mongo_db.DynamicDocument):
    """角色表"""
    name = mongo_db.StringField(required=True, max_length=256)
    role_type = mongo_db.IntField(default=0, choices=ROLE_TYPE, unique=True)
    operation_permissions = mongo_db.ListField(default=list())
    create_time = mongo_db.DateTimeField(default=datetime.utcnow)
    update_time = mongo_db.DateTimeField(default=datetime.utcnow)

    def to_dict(self):
        """
        将Role对象转换为python字典对象
        :return: dict
        """
        new_role = dict(
            name=self.name,
            role_type=self.role_type,
            operation_permissions=self.operation_permissions
        )
        return new_role


class Permission(mongo_db.DynamicDocument):
    """权限表"""
    name = mongo_db.StringField(required=True, max_length=256)
    action = mongo_db.StringField(required=True, max_length=256)
    create_time = mongo_db.DateTimeField(default=datetime.utcnow)
    update_time = mongo_db.DateTimeField(default=datetime.utcnow)
    is_deleted = mongo_db.BooleanField(default=False)
