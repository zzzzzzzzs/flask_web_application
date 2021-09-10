"""
项目应用各个模块的初始化
"""
import os
from flask import Flask
from flask_mongoengine import MongoEngineSessionInterface
from flask_debugtoolbar import DebugToolbarExtension
from configs import config_obj
from api import api, login_manager
from model import mongo_db, redis_db

section_app = config_obj['APP']
# -------------------------Init Flask app-----------------------
app = Flask(__name__)
app.debug = bool(section_app['DEBUG'])
app.host = section_app['HOST']
app.port = int(section_app['PORT'])

# Set session configs
app.session_cookie_name = 'sessionId'
app.secret_key = section_app['SECRET_KEY']

# app.config['SWAGGER_UI_JSONEDITOR'] = True
app.config['BUNDLE_ERRORS'] = True
api.init_app(app)

# -------------------------Init DB-----------------------
app.config['MONGODB_SETTINGS'] = config_obj['mongodb']
app.session_interface = MongoEngineSessionInterface(mongo_db)
mongo_db.init_app(app)

# -------------------------Init Redis DB-----------------------
app.config['REDIS_URL'] = config_obj['REDIS']['REDIS_URL']
redis_db.init_app(app)

# -------------------------Init Login Manager-----------------------
login_manager.init_app(app)

# -------------------------Init Toolbar-----------------------
app.config['DEBUG_TB_PROFILER_ENABLED'] = True
toolbar = DebugToolbarExtension()
toolbar.init_app(app)


# -------------------------custom errorhandler --------------------
@app.errorhandler(400)
def handle_400(e):
    return e.description, 400


@app.errorhandler(401)
def handle_401(e):
    return e.description, 401


@app.errorhandler(403)
def handle_403(e):
    return e.description, 403