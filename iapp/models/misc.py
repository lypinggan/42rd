# -*- coding: utf-8 -*-
import hashlib

from datetime import datetime

from flaskext.sqlalchemy import BaseQuery

from iapp.extensions import db
from iapp.permissions import null
from iapp.models.permissions import Permissions
from iapp.models import User




class Upload_FileQuery(BaseQuery):
    def all_list(self):
        return self.order_by(Upload_File.id.desc())

'''
文件上传记录
'''
class Upload_File(db.Model):
    
    __tablename__ = "upload_file"
    query_class = Upload_FileQuery

    id = db.Column(db.Integer, primary_key=True)
    
    #发生时间
    date_created = db.Column(db.DateTime, default=datetime.now)
    
    #上传者ID
    user_id = db.Column(db.Integer)

    #文件后缀
    file_type = db.Column(db.Integer)
    
    #文件名字
    file_old_name = db.Column(db.String(250),default=u'')
    
    file_new_name = db.Column(db.String(250),default=u'')

    def __init__(self, user_id, file_type, file_old_name, file_new_name):
        self.user_id = user_id
        self.file_type = file_type
        self.file_old_name = file_old_name
        self.file_new_name = file_new_name
