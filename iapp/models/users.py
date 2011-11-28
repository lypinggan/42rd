# -*- coding: utf-8 -*-
import hashlib

from datetime import datetime

from werkzeug import generate_password_hash, check_password_hash, \
    cached_property

from flaskext.sqlalchemy import BaseQuery
from flaskext.principal import RoleNeed, UserNeed, Permission

from iapp.extensions import db
from iapp.permissions import null
from iapp.models.permissions import Permissions

class UserQuery(BaseQuery):

    def from_identity(self, identity):
        try:
            user = self.get(int(identity.name))
        except ValueError:
            user = None
        if user:
            identity.provides.update(user.provides)
        identity.user = user
        return user
 
    def authenticate(self, login, password):
        
        user = self.filter(db.or_(User.username==login,
                                  User.email==login)).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated
    #根据username获取信息
    def username_get_info(self, username):
        info = self.filter(User.username==username).\
                first()
        if info is None:
            abort(404)
        else:
            return info


class User(db.Model):
    
    __tablename__ = "users"

    query_class = UserQuery

    # user roles
    MEMBER = 100
    MODERATOR = 200
    ADMIN = 300

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Integer, default=MEMBER)#权限
    prestige = db.Column(db.Integer, default=0)#威望
    integral = db.Column(db.Integer, default=0)#积分
    username = db.Column(db.Unicode(60), unique=True, nullable=False)#用户名
    email = db.Column(db.String(150), unique=True, nullable=False)#邮箱地址
    avatar = db.Column(db.String(150),default='no.jpg')#头像路径
    _password = db.Column("password", db.String(80), nullable=False)#密码
    thank = db.Column(db.Integer, default=0)#获得多少感谢
    date_joined = db.Column(db.DateTime, default=datetime.now)
    activation_key = db.Column(db.String(80), unique=True)#激活时需要的KEY
    unread_message = db.Column(db.Integer,default=0)#未读信息条数
    followers = db.Column(db.Integer,default=0)#被关注
    following = db.Column(db.Integer,default=0)#关注
    question_number = db.Column(db.Integer,default=0)#提问数
    answering = db.Column(db.Integer,default=0)#回答数
    best_answer_number = db.Column(db.Integer,default=0)#最佳答案数
    tagline = db.Column(db.String(150),default=u'42ic社区会员')#最能概括你的标志性语言
    description = db.Column(db.UnicodeText)
    name = db.Column(db.String(150),default=u'请修改名片')#姓名
    phone = db.Column(db.String(150),default='')#电话
    city = db.Column(db.String(150),default='')#城市
    address = db.Column(db.String(300),default='')#详细地址
    #reg_ip = db.Column(db.Unicode(20))


    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    @cached_property
    def permissions(self):
        return self.Permissions(self)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    password = db.synonym("_password", 
                          descriptor=property(_get_password,
                                              _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    @property
    def is_moderator(self):
        return self.role >= self.MODERATOR

    @property
    def is_admin(self):
        return self.role >= self.ADMIN
    @cached_property
    def provides(self):
        needs = [RoleNeed('authenticated'),
                 UserNeed(self.id)]

        if self.is_moderator:
            needs.append(RoleNeed('moderator'))

        if self.is_admin:
            needs.append(RoleNeed('admin'))

        return needs

    def avatar_url(self):
        return "/static/avatar"+self.avatar


class users_iconQuery(BaseQuery):
    pass
class Users_icon(db.Model):
    
    __tablename__ = "users_icon"

    query_class = users_iconQuery

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    x = db.Column(db.Integer,default=0)
    y = db.Column(db.Integer,default=0)
    h = db.Column(db.Integer,default=45)
    image_name = db.Column(db.String(150),default='no.jpg')
    date_joined = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, *args, **kwargs):
        super(Users_icon, self).__init__(*args, **kwargs)
'''
用户关注问题列表
'''
class User_FollowQuery(BaseQuery):
    pass
class User_Follow(db.Model):

    __tablename__ = "user_follow"
    query_class = User_FollowQuery
    
    id = db.Column(db.Integer, primary_key=True)
    #主、被关注者
    main_id = db.Column(db.Integer, 
                          db.ForeignKey(User.id, ondelete='CASCADE'), 
                          nullable=False)
    #从、跟随者
    follower_id = db.Column(db.Integer, 
                          db.ForeignKey(User.id, ondelete='CASCADE'), 
                          nullable=False)
    def __init__(self, main_id, follower_id):
        self.main_id = main_id
        self.follower_id = follower_id



class User_MessageQuery(BaseQuery):
    def get_my_list(self,user_id):
        return self.filter(User_Message.user_id == user_id).order_by(User_Message.id.desc())
class User_Message(db.Model):
    
    __tablename__ = "users_message"

    query_class = User_MessageQuery

    id = db.Column(db.Integer, primary_key=True)
    #用户ID
    user_id = db.Column(db.Integer)
    #信息标题
    title = db.Column(db.String(250),default=u'42ic消息')
    #消息内容
    content = db.Column(db.UnicodeText)
    #消息创建时间
    date_created = db.Column(db.DateTime, default=datetime.now)
    #是否未读
    unread = db.Column(db.Integer)#1=未读，0=已读

    def __init__(self, user_id, title, content ):
        self.user_id = user_id
        self.title = title
        self.content = content
        self.unread = 1
