from flaskext.mail import Mail
from flaskext.sqlalchemy import SQLAlchemy
from iapp.utils import Cache, Queue

__all__ = ['cache', 'mail', 'db', 'queue']

mail = Mail()
db = SQLAlchemy()
cache = Cache()
queue = Queue()

