import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SESSION_TYPE = 'filesystem'
SESSION_KEY = 'very secret key'
DEBUG=True
CACHE_MEMCACHED_SERVERS =['127.0.0.1:11211']
