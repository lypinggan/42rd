# -*- coding: utf-8 -*-
import random, string, time, os
from flask import Module, url_for, \
    redirect, g, flash, request, current_app, abort

from flaskext.mail import Message
from flaskext.babel import gettext as _

from iapp.extensions import mail, db, cache

from iapp.helpers import render_template, cached
from iapp.decorators import keep_login_url
from iapp.permissions import auth

frontend = Module(__name__)

'''
首页
'''
@frontend.route("/", methods=("GET", "POST"))
def index():
    return render_template( 'index.html')
