"""
初始化mongodb-client实例
"""
from flask_mongoengine import MongoEngine
from flask_redis import FlaskRedis

mongo_db = MongoEngine()
redis_db = FlaskRedis()
