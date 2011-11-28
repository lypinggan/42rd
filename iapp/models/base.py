# -*- coding: utf-8 -*-
from mongoengine import QuerySet, DoesNotExist, MultipleObjectsReturned
from flaskext.sqlalchemy import Pagination

class BaseQuerySet(QuerySet):
    """
    Custom QuerySet with some handy extra methods. Use this or 
    subclass of this with models:

    class MyClass(Document):
        ...
        meta = {'queryset_class' : BaseQuerySet})
    """

    def get_or_404(self, **kwargs):
        try:
            return self.get(**kwargs)
        except (DoesNotExist, MultipleObjectsReturned):
            abort(404)

    def first_or_404(self, **kwargs):
        result = self.first()
        if result is None:
            abort(404)
'''
分页函数：
page=当前第几页
per_page=一页显示多少项


'''
    def paginate(self, page, per_page=20, error_out=True):
        """Returns `per_page` items from page `page`.  By default it will
        abort with 404 if no items were found and the page was larger than
        1.  This behavor can be disabled by setting `error_out` to `False`.

        Returns an :class:`Pagination` object.
        """
        if error_out and page < 1:
            abort(404)
        items = self.limit(per_page).skip((page - 1) * per_page).all()
        if not items and page != 1 and error_out:
            abort(404)
        return Pagination(self, page, per_page, self.count(), items)
