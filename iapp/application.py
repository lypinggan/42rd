# -*- coding: utf-8 -*-
"""
"""
import os
import logging
from timeit import default_timer
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask, Response, request, g, \
        jsonify, redirect, url_for, flash

from flaskext.babel import Babel, gettext as _
from flaskext.principal import Principal, identity_loaded

from iapp import helpers
from iapp import views
from iapp.config import DefaultConfig
from iapp.helpers import render_template
from iapp.extensions import db, mail, cache

__all__ = ["create_app"]

DEFAULT_APP_NAME = "iapp"

#定义URL分发
DEFAULT_MODULES = (
    (views.frontend, ""),
    (views.account, "/account"),
)

#创建应用
def create_app(config=None, app_name=None, modules=None):

    if app_name is None:
        app_name = DEFAULT_APP_NAME

    if modules is None:
        modules = DEFAULT_MODULES

    app = Flask(app_name)

    configure_app(app, config)

    configure_logging(app)
    configure_errorhandlers(app)
    configure_extensions(app)
    configure_before_handlers(app)
    configure_template_filters(app)
    configure_context_processors(app)
    # configure_after_handlers(app)
    configure_modules(app, modules)

    return app

#加载配置
def configure_app(app, config):
    
    app.config.from_object(DefaultConfig())

    if config is not None:
        app.config.from_object(config)

    app.config.from_envvar('APP_CONFIG', silent=True)

#加载模块
def configure_modules(app, modules):
    
    for module, url_prefix in modules:
        app.register_module(module, url_prefix=url_prefix)

#定义模板过滤函数
def configure_template_filters(app):

    @app.template_filter()
    def timesince(value):
        return helpers.timesince(value)
    @app.template_filter()
    def for_tags(value):
        return helpers.for_tags(value)
    @app.template_filter()
    def markdown(value):
        return helpers.markdown(value)
    @app.template_filter()
    def avatar_url(value):
        return helpers.avatar_url(value)
    @app.template_filter()
    def tohtml(value):
        return helpers.tohtml(value)
    
#定义加载时预处理
def configure_before_handlers(app):

    @app.before_request
    def authenticate():
        g.user = getattr(g.identity, 'user', None)


def configure_context_processors(app):

    @app.context_processor
    def get_tags():
        '''
        #tags = cache.get("tags")
        if tags is None:
            tags = {}#Tag.query.order_by(Tag.num_posts.desc()).limit(13).all()
            #cache.set("tags", tags)
        '''
        tags = {}
        return dict(tags=tags)
        

    @app.context_processor
    def config():
        return dict(config=app.config)

#
def configure_extensions(app):

    mail.init_app(app)
    db.init_app(app)
    cache.init_app(app)
    # more complicated setups
    configure_identity(app)
    

def configure_identity(app):

    Principal(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        g.user = User.query.from_identity(identity)


#定义错误页面
def configure_errorhandlers(app):

    if app.testing:
        return

    @app.errorhandler(404)
    def page_not_found(error):
        if request.is_xhr:
            return jsonify(error=u"对不起,页面没有找到.")
        return render_template("errors/404.html", error=error)

    @app.errorhandler(403)
    def forbidden(error):
        if request.is_xhr:
            return jsonify(error=u"对不起,您没有权限")
        return render_template("errors/403.html", error=error)

    @app.errorhandler(500)
    def server_error(error):
        if request.is_xhr:
            return jsonify(error=u"不好意思,服务器开小差了.")
        return render_template("errors/500.html", error=error)

    @app.errorhandler(401)
    def unauthorized(error):
        if request.is_xhr:
            return jsonfiy(error=u"请先登陆")
        flash(u"请登陆后再查看这个页面", "error")
        return redirect(url_for("account.login", next=request.path))

#日志处理
def configure_logging(app):
    if app.debug or app.testing:
        return

    mail_handler = \
        SMTPHandler(app.config['MAIL_SERVER'],
                    '11939053@qq.com',
                    app.config['ADMINS'], 
                    'application error',
                    (
                        app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'],
                    ))

    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    debug_log = os.path.join(app.root_path, 
                             app.config['DEBUG_LOG'])

    debug_file_handler = \
        RotatingFileHandler(debug_log,
                            maxBytes=100000,
                            backupCount=10)

    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    error_log = os.path.join(app.root_path, 
                             app.config['ERROR_LOG'])

    error_file_handler = \
        RotatingFileHandler(error_log,
                            maxBytes=100000,
                            backupCount=10)

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)



