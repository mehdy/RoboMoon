#!robo/bin/python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path

db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

u = models.User(username = 'admin', password = sha256('admin').hexdigest(), email = 'admin@robomoon.com')
db.session.add(u)
db.session.commit()

print 'The database has been successfully created.'
print 'the admin user info is:'
print 'username: admin'
print 'password: admin'
print 'you can change your username and password in /cpanel/users/admin'