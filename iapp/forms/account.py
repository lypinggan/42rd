# -*- coding: utf-8 -*-
from flaskext.wtf import Form, HiddenField, BooleanField, TextField, TextAreaField, \
        PasswordField, SubmitField, TextField, RecaptchaField, \
        ValidationError, required, email, equal_to, regexp

from flaskext.babel import gettext, lazy_gettext as _ 

from iapp.models import User
from iapp.extensions import db

from .validators import is_username

class LoginForm(Form):
    next = HiddenField()
    remember = BooleanField(u"记住我")
    login = TextField(
        u"用户名或邮箱地址", 
        validators=[
            required(
                message= u"请输入一个有效的邮箱地址"
            )
        ]
    )

    password = PasswordField( u"密码" )

    submit = SubmitField( u"登 陆" )

class SignupForm(Form):

    next = HiddenField()
    username = TextField(u"用户名", validators=[
                         required(message=u"用户名必须"), 
                         is_username])

    password = PasswordField(u"密码", validators=[
                             required(message=u"请输入有效的密码")])

    password_again = PasswordField(u"密码确认", validators=[
                                   equal_to("password", message=\
                                            u"密码确认无效")])
    email = TextField(u"邮箱地址", validators=[
                      required(message=u"邮箱地址格式无效")])


    submit = SubmitField(u"注 册")

    def validate_username(self, field):
        user = User.query.filter(User.username.like(field.data)).first()
        if user:
            raise ValidationError, u"用户名已经被使用"

    def validate_email(self, field):
        user = User.query.filter(User.email.like(field.data)).first()
        if user:
            raise ValidationError, u"邮箱地址已经被使用"


class EditAccountForm(Form):


    email = TextField(u"E-mail地址", validators=[
                      required(message=u"邮箱地址是必须的"),
                      email(message=u"一个有效的邮箱地址是必须的")])

    #receive_email = BooleanField(u"接收来自朋友的私人邮件")
    
    #email_alerts = BooleanField(u"当别人回复我的文章时，使用邮箱发给我")
    tagline = TextField(u"一句话概况我")
    description = TextAreaField(u"个人简介")

    submit = SubmitField(u"保存!")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs['obj'] = self.user
        super(EditAccountForm, self).__init__(*args, **kwargs)
    '''
    def validate_username(self, field):
        user = User.query.filter(db.and_(
                                 User.username.like(field.data),
                                 db.not_(User.id==self.user.id))).first()
        if user:
            raise ValidationError, u"用户名已经被使用"
    '''
    def validate_email(self, field):
        user = User.query.filter(db.and_(
                                 User.email.like(field.data),
                                 db.not_(User.id==self.user.id))).first()
        if user:
            raise ValidationError, u"邮箱地址已经被使用"

class RecoverPasswordForm(Form):

    email = TextField(u"我注册时的邮箱地址", validators=[
                      email(message=u'请输入一个有效的电子邮件地址')])

    submit = SubmitField(u"确定邮箱地址,提交申请!")


class ChangePasswordForm(Form):

    activation_key = HiddenField()

    password = PasswordField(u"新密码", validators=[
                             required(message=u"密码必须")])
    
    password_again = PasswordField(u"重复密码", validators=[
                                   equal_to("password", message=\
                                            u"两次密码不相同")])

    submit = SubmitField(u"确认，修改!")
class EditNameCardForm(Form):
    name = TextField(u"姓名")
    phone = TextField(u"电话")
    city = TextField(u"城市")
    address = TextField(u"详细地址")
    submit = SubmitField(u"确认，修改!")
    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs['obj'] = self.user
        super(EditNameCardForm, self).__init__(*args, **kwargs)

class DeleteAccountForm(Form):

    submit = SubmitField(u"我想好了,真的要删除帐号!")


