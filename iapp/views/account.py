# -*- coding: utf-8 -*-
import uuid
import time
import os
import random, string
from flask import Module, flash, request, g, current_app, \
    abort, redirect, url_for, session, jsonify

from flaskext.mail import Message
from flaskext.babel import gettext as _
from flaskext.principal import identity_changed, Identity, AnonymousIdentity

from iapp.helpers import render_template, md5
from iapp.extensions import db, mail
from iapp.permissions import auth
from iapp.utils.pic import picopen, pic_square

'''
账户首页
自动跳转资料页面
'''
account = Module(__name__)
@account.route("/")
def home():
    return redirect('')
