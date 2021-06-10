"""
    Description: 用户视图处理逻辑
    :author: zouzhisheng
    :copyright: (c) 2021, Tungee
    :date created: 2021-06-08
    :python version: 3.5
"""
import os
from model.user import User
from pymongo.errors import ServerSelectionTimeoutError
from mongoengine.errors import NotUniqueError, DoesNotExist, ValidationError
from bson.errors import InvalidId
from flask_login import login_user, current_user
from utils.logger import log
from utils.permission import auth, QUERY_ALL_USER
from utils import make_response_data
from utils.status_code import UserStatusCode, BasicStatusCode
from configs import config_obj
from PIL import Image


def logic_sign_up(args):
    """
    用户注册逻辑
    :param args: dict 已经被解析的请求，
    :return: ok->bool, status_code->int, msg
    """
    try:
        if args['password'] != args['confirm_password']:
            raise ValueError('两次密码不一致')

        User(
            nick_name=args['nick_name'],
            real_name=args['real_name'],
            phone=args['phone'],
            password=args['password'],
            avatar=config_obj['project']['avatar_default_url'],
            is_deleted=False
        ).save()
    except ServerSelectionTimeoutError as e:    # pylint: disable=C0103
        log.logger.error(repr(e))
        return False, 500, make_response_data(**BasicStatusCode.TIMEOUT_ERROR)
    except NotUniqueError:
        return False, 400, make_response_data(**UserStatusCode.EXISTED_ERROR, message="该号码已存在")
    except ValueError as e:
        return False, 400, make_response_data(**UserStatusCode.PASSWORD_ERROR, message=str(e))
    except ValidationError as e:
        fields = ','.join([k for k in e.errors.keys()])
        message = "参数：{} 格式错误".format(fields)
        return False, 401, make_response_data(code=UserStatusCode.INVALID_ARGS['code'], message=message)
    except Exception as e:  # pylint: disable=C0103
        log.logger.error(repr(e))
        return False, 500, make_response_data(**BasicStatusCode.SERVER_ERROR)

    return True, 200, make_response_data()


def logic_login_in(args):
    """
    用户登录逻辑
    :param args: dict 已经被解析的请求，
    :return: ok->bool, status_code->int, msg
    """
    try:
        user = User.objects.get(phone=args['phone'])
    except DoesNotExist:
        return False, 400, make_response_data(**UserStatusCode.NOT_EXIST_ERROR, message="用户不存在")

    if not user.password_is_correct(args['password']):
        return False, 400, make_response_data(**UserStatusCode.WRONG_PWD_OR_ACCOUNT)

    # 登录流程
    if not current_user.is_authenticated:
        login_user(user)

    return True, 200, make_response_data(user)


def logic_rename_image(user_id, image_name):
    """
    重命名
    :param user_id:
    :param image_name:
    :return: str
    """
    image_ext_name = os.path.splitext(image_name)[-1]
    return "{}{}".format(user_id, image_ext_name)


def logic_resize_and_save_image(image_name, image_obj):
    """
    裁剪并保存图片
    :param image_name:
    :param image_obj:
    :return: ok, image_path
    """
    image = Image.open(image_obj)
    new_image = image.resize(
        (
            config_obj['project']['avatar_width'],
            config_obj['project']['avatar_height']
        )
    )
    image_full_path = os.path.join(
        config_obj['project']['temp_data_root'],
        config_obj['project']['avatar_path'],
        image_name
    )
    avatar_url = os.path.join(
        config_obj['project']['avatar_path'],
        image_name
    )
    try:
        new_image.save(image_full_path)
    except Exception as e:
        log.logger.error(repr(e))
        return False, avatar_url
    else:
        return True, avatar_url


def logic_upload_avatar(user, args):
    """
    用户上传头像处理逻辑
    :param user: 用户对象
    :param args: dict 已经被解析的请求
    :return: msg->str, status_code->int, ok->bool
    """
    image_obj = args.get('avatar', None)
    if not image_obj:
        return False, 400, make_response_data(**BasicStatusCode.INVALID_ARGS)
    # 图片重命名
    new_image_name = logic_rename_image(str(user.id), image_obj.filename)
    # 压缩图片并保存
    ok, msg = logic_resize_and_save_image(new_image_name, image_obj)
    if not ok:
        return ok, 500, make_response_data(msg)
    # 数据入库
    user.update(avatar=msg)
    try:
        user.save()
    except Exception as e:
        log.logger.error(repr(e))
        return False, 500, make_response_data(**BasicStatusCode.DATABASE_ERROR)
    # 重新获取用户数据
    user.reload()
    return True, 201, make_response_data(user.avatar)


def logic_query_users(args):
    """
    查询用户信息
    :param args: dict 已经被解析的请求
    :return:
    """
    user_id = args.get('user_id')
    page = args.get('page')
    page_size = args.get('page_size')

    start = page * page_size
    end = start + page_size
    if user_id:
        # 查看单个用户
        users = User.objects.filter(id=user_id)
    else:
        # 查看所有用户
        # 进行权限判断，只能看角色比自己小的用户
        users = auth(QUERY_ALL_USER)(User.objects.filter)(
            role_type__lt=current_user.role_type,
            is_deleted=False
        )[start:end]
    try:
        users = list(users)
        for user in users:
            user.role_type_name = user.get_role_type_display()
    except (ValidationError, InvalidId) as e:
        log.logger.error(repr(e))
        return False, 400, make_response_data(**UserStatusCode.INVALID_USER_ID)

    return True, 200, make_response_data(users)


def logic_update_user_info(args):
    """
    修改某个用户个人信息
    :param args: dict 已经被解析的请求
    :return: ok, status_code, msg
    """
    _id = args.pop('user_id')
    try:
        user = User.objects.get(pk=_id)
    except DoesNotExist:
        return False, 400, make_response_data(**UserStatusCode.INVALID_USER_ID)
    user.modify(**args)
    user = user.reload()
    return True, 201, make_response_data(user)


def logic_check_role_type_and_permission(role_type):
    """
    判断当前用户是否有创建对应角色用户的权限，只能创建角色比自己小的用户
    但超级管理员可以创建超级管理员
    :param role_type: int
    :return:
    """
    user = current_user
    if user.role_type != config_obj['ROLE']['SUPER_ADMIN']:
        # 如果当前用户不是超级管理员

        if user.role_type <= role_type:
            return False, '无权限创建新用户'

    return True, 'ok'


def logic_create_user(args):
    """
    添加用户
    :param args: dict 已经被解析的请求
    :return: ok, status_code, msg
    """
    role_type = args.get('role_type')
    ok, msg = logic_check_role_type_and_permission(role_type)
    if not ok:
        return False, 400, make_response_data(**UserStatusCode.PERMISSION_NOT_ALLOW)

    try:
        User(
            nick_name=args['nick_name'],
            real_name=args['real_name'],
            phone=args['phone'],
            password=args['password'],
            avatar=config_obj['project']['avatar_default_url'],
            role_type=args['role_type'],
            is_deleted=False
        ).save()
    except ServerSelectionTimeoutError as e:    # pylint: disable=C0103
        log.logger.error(repr(e))
        return False, 500, make_response_data(**BasicStatusCode.TIMEOUT_ERROR)
    except NotUniqueError:
        return False, 400, make_response_data(**UserStatusCode.EXISTED_ERROR, message="该号码已存在")
    except ValueError as e:
        return False, 400, make_response_data(**UserStatusCode.PASSWORD_ERROR, message=str(e))
    except Exception as e:  # pylint: disable=C0103
        log.logger.error(repr(e))
        return False, 500, make_response_data(**BasicStatusCode.SERVER_ERROR)

    return True, 200, make_response_data()