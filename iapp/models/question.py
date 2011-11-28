# -*- coding: utf-8 -*-
'''
问题部分
'''
import random
import time

from datetime import datetime

from werkzeug import cached_property

from flask import url_for, Markup,g,abort
from flaskext.sqlalchemy import BaseQuery
from flaskext.principal import Permission, UserNeed, Denial

from iapp.extensions import db
from iapp.helpers import slugify, domain, markdown
from iapp.permissions import auth, moderator
from iapp.models.permissions import Permissions
from iapp.models.users import User


class QuestionQuery(BaseQuery):

    def jsonify(self):
        for post in self.all():
            yield post.json
    #最新
    def latest(self):
        return self.filter(Question.deleteed == 0 ).order_by(Question.sort.desc(),Question.id.desc())
    #最热
    def hottest(self):
        return self.filter(Question.deleteed == 0 ).order_by(Question.votes.desc(),Question.id.desc())
    #最近一个月最热
    def hotmonth(self):
        return self.filter(Question.deleteed == 0 ).order_by(Question.sort.desc(),Question.id.desc())
    #等待回答
    def unanswered(self):
        return self.filter(Question.deleteed == 0 ).filter(Question.answer_id == 0).order_by(Question.id.desc())
    #我的提问
    def my_questions(self):
        try:
            return self.filter(Question.author_id == g.user.id ).\
                        filter(Question.deleteed == 0 ).order_by(Question.votes.desc(),Question.id.desc())
        except:
            abort(404)
            
    def search(self, keywords):
        criteria = []
        for keyword in keywords.split():

            keyword = '%' + keyword + '%'

            criteria.append(db.or_(Question.title.ilike(keyword),
                                   Question.description.ilike(keyword)))

        q = reduce(db.and_, criteria)
        return self.filter(q).order_by(Question.votes.desc(),Question.id.desc())


class Question(db.Model):

    __tablename__ = "question"
    

    PER_PAGE = 30
    query_class = QuestionQuery
    
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, 
                          db.ForeignKey(User.id, ondelete='CASCADE'), 
                          nullable=False)
    author = db.relation(User, innerjoin=True, lazy="joined")
    title = db.Column(db.Unicode(256))
    description = db.Column(db.UnicodeText)
    date_created = db.Column(db.DateTime, default=datetime.now)#创建时间
    answer_id = db.Column(db.Integer, default=0)#正确答案ID
    num_answer = db.Column(db.Integer, default=0)#答案个数
    num_follow = db.Column(db.Integer, default=0)#关注次数
    votes = db.Column(db.Integer, default=0)#得票，也是喜欢
    views = db.Column(db.Integer, default=0)#查看次数
    deleteed = db.Column(db.Integer, default=0)#=1为删除
    sort = db.Column(db.Integer, default=int(time.time()))#排序，从大到小
    _tags = db.Column("tags", db.UnicodeText)
    
    __mapper_args__ = {'order_by' : id.desc()}
    

    def __init__(self, *args, **kwargs):
        self.author_id = g.user.id
        super(Question, self).__init__(*args, **kwargs)

    def _get_tags(self):
        return self._tags 

    def _set_tags(self, tags):
        self._tags = tags
        if self.id:
            # ensure existing tag references are removed
            d = db.delete(question_tags, question_tags.c.question_id==self.id)
            db.engine.execute(d)
        for tag in set(self.taglist):
            slug = slugify(tag)
            tag_obj = Tag.query.filter(Tag.slug==slug).first()
            if tag_obj is None:
                tag_obj = Tag(name=tag, slug=slug)
                db.session.add(tag_obj)
            if self not in tag_obj.question:
                tag_obj.question.append(self)
    
    tags = db.synonym("_tags", descriptor=property(_get_tags, _set_tags))

    @property
    def taglist(self):
        if self.tags is None:
            return []
        tags = [t.strip() for t in self.tags.split(",")]
        return [t for t in tags if t]


question_tags = db.Table("question_tags", db.Model.metadata,
    db.Column("question_id", db.Integer, 
              db.ForeignKey('question.id', ondelete='CASCADE'), 
              primary_key=True),
    db.Column("tag_id", db.Integer, 
              db.ForeignKey('tags.id', ondelete='CASCADE'),
              primary_key=True))


class TagQuery(BaseQuery):
    def tags_search(self, keywords):

        criteria = []

        for keyword in keywords.split():

            keyword = '%' + keyword + '%'

            criteria.append(db.or_(Tag.slug.ilike(keyword),
                                   Tag.description.ilike(keyword)))
        q = reduce(db.and_, criteria)
        return self.filter(q).distinct()
class Tag(db.Model):

    __tablename__ = "tags"
    
    query_class = TagQuery

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.Unicode(80), unique=True)
    description = db.Column(db.UnicodeText)#标签描述
    question = db.dynamic_loader(Question, secondary=question_tags, query_class=QuestionQuery)

    _name = db.Column("name", db.Unicode(80), unique=True)
    
    def __str__(self):
        return self.name

    def _get_name(self):
        return self._name

    def _set_name(self, name):
        self._name = name.lower().strip()
        self.slug = slugify(name)

    name = db.synonym("_name", descriptor=property(_get_name, _set_name))

    def url(self):
        return url_for("frontend.tag", slug=self.slug)

    num_question = db.column_property(
        db.select([db.func.count(question_tags.c.question_id)]).\
            where(db.and_(question_tags.c.tag_id==id,
                          Question.id==question_tags.c.question_id)).as_scalar())
'''
用户关注问题列表
'''
class Question_FollowQuery(BaseQuery):
    def is_following(self, question_id, user_id):
        f = self.filter( Question_Follow.question_id==question_id).filter(Question_Follow.user_id==user_id ).all()
        if f :
            return True
        else:
            return False
class Question_Follow(db.Model):

    __tablename__ = "question_follow"
    query_class = Question_FollowQuery
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, 
                          db.ForeignKey(User.id, ondelete='CASCADE'), 
                          nullable=False)
    question_id = db.Column(db.Integer, 
                          db.ForeignKey(Question.id, ondelete='CASCADE'), 
                          nullable=False)
    def __init__(self, user_id, question_id):
        self.user_id = user_id
        self.question_id = question_id
'''
用户喜欢问题列表
'''
class Question_VotesQuery(BaseQuery):
    def is_voteing(self, question_id, user_id):
        f = self.filter( Question_Votes.question_id==question_id).filter(Question_Votes.user_id==user_id ).all()
        if f :
            return True
        else:
            return False
    def f(self, question_id, user_id):
        return self.filter( Question_Votes.question_id==question_id).filter(Question_Votes.user_id==user_id ).first()
class Question_Votes(db.Model):

    __tablename__ = "question_votes"
    query_class = Question_VotesQuery
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, 
                          db.ForeignKey(User.id, ondelete='CASCADE'), 
                          nullable=False)
    question_id = db.Column(db.Integer, 
                          db.ForeignKey(Question.id, ondelete='CASCADE'), 
                          nullable=False)
    def __init__(self, user_id, question_id):
        self.user_id = user_id
        self.question_id = question_id



'''
问题答案表
'''
class AnswerQuery(BaseQuery):
    #答案列表
    def answer_list(self, question_id):
        return self.filter(Answer.question_id == question_id).order_by(Answer.answer_ok.desc(), Answer.id.asc())
        
class Answer(db.Model):
    __tablename__ = "answer"
    PER_PAGE = 40
    query_class = AnswerQuery

    id = db.Column(db.Integer, primary_key=True)
    #所属问题ID
    question_id = db.Column(db.Integer, default=0)
    #答案作者ID
    author_id = db.Column(db.Integer, 
                          db.ForeignKey(User.id, ondelete='CASCADE'), 
                          nullable=False)
    author = db.relation(User, innerjoin=True, lazy="joined")
    #答案内容
    answer = db.Column(db.UnicodeText)
    #创建时间
    date_created = db.Column(db.DateTime, default=datetime.now)
    #最后修改时间
    date_lastedit = db.Column(db.DateTime, default=datetime.now)
    #是否满意答案=1为最终答案
    answer_ok = db.Column(db.Integer, default=0)
    #评论次数
    num_comment = db.Column(db.Integer, default=0)
    #得票
    num_votes = db.Column(db.Integer, default=0)
    #感谢次数
    unm_thank = db.Column(db.Integer, default=0)
    #=1为删除
    deleteed = db.Column(db.Integer, default=0)
    #排序，从大到小
    sort = db.Column(db.Integer, default=int(time.time()))
    #发布IP
    ip = db.Column(db.Unicode(20))
    
    def __init__(self, *args, **kwargs):
        self.author_id = g.user.id
        super(Answer, self).__init__(*args, **kwargs)
'''
答案评论表
'''
class Answer_CommentQuery(BaseQuery):
    pass        
class Answer_Comment(db.Model):
    __tablename__ = "answer_comment"
    PER_PAGE = 40
    query_class = Answer_CommentQuery

    id = db.Column(db.Integer, primary_key=True)
    #所属答案ID
    answer_id = db.Column(db.Integer, default=0)
    #评论作者ID
    author_id = db.Column(db.Integer, 
                          db.ForeignKey(User.id, ondelete='CASCADE'), 
                          nullable=False)
    author = db.relation(User, innerjoin=True, lazy="joined")
    #评论内容
    content = db.Column(db.UnicodeText)
    #创建时间
    date_created = db.Column(db.DateTime, default=datetime.now)

    #=1为删除
    deleteed = db.Column(db.Integer, default=0)
    
    #发布IP
    #ip = db.Column(db.Unicode(20),default= request.remote_addr)
    
    def __init__(self, answer_id, author_id, content):
        self.answer_id = answer_id
        self.author_id = author_id
        self.content = content

'''
用户感谢答案列表
用户的感谢记录
'''
class Answer_ThankQuery(BaseQuery):
    pass

class Answer_Thank(db.Model):
    __tablename__ = "Answer_thank"
    query_class = Answer_ThankQuery
    
    id = db.Column(db.Integer, primary_key=True)
    #感谢用户
    user_id = db.Column(db.Integer, 
                          db.ForeignKey(User.id, ondelete='CASCADE'), 
                          nullable=False)
    #被感谢的答案
    answer_id = db.Column(db.Integer, 
                          db.ForeignKey(Answer.id, ondelete='CASCADE'), 
                          nullable=False)
    def __init__(self, user_id, answer_id):
        self.user_id = user_id
        self.answer_id = answer_id
