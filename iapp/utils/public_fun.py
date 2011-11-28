# -*- coding: utf-8 -*-
"""
    helpers.py
    ~~~~~~~~
    Helper functions for 42ic
    :copyright: (c) 2010 by lyping gan
    :license: BSD, see LICENSE for more details.
"""
import time
from datetime import datetime

from flask import current_app, g, render_template as rt, url_for

from flaskext.babel import gettext, ngettext

from iapp.extensions import cache
from iapp.extensions import db, mail
from iapp.models import User_Message,User

"""
获取我定义的数据库ID类型
有一定的唯一性
"""
def get_my_id():
    return int (time.time()*31415-30000000000000)

"""
给用户发送站内信息
send_msg(用户ID，标题，内容)
"""
def send_msg( uid, title, content ):
    msg = User_Message(uid, title, content)
    db.session.add( msg )
    user = User.query.filter(User.id == uid ).first()
    user.unread_message =user.unread_message+1
    db.session.commit()
    
