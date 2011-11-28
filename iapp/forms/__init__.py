# -*- coding: utf-8 -*-
"""
    forms.py
    ~~~~~~~~

    Description of the module goes here...

    :copyright: (c) 2010 by lyping gan
    :license: BSD, see LICENSE for more details.
"""

from .account import LoginForm, SignupForm, EditAccountForm, \
        RecoverPasswordForm, ChangePasswordForm, DeleteAccountForm, EditNameCardForm

from .question import Question_AskForm, Question_EditForm, Answer_EditForm

from .group import Group_New_TopicForm, Group_Topic_New_ReplyForm,\
                    Group_RequisitionForm, Group_EditForm, Group_Edit_TopicForm

#from .contact import ContactForm, MessageForm
#from .comment import CommentForm, CommentAbuseForm
