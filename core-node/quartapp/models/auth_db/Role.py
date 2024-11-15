from mongoengine import Document, connect
from mongoengine.fields import (
    BinaryField,
    BooleanField,
    DateTimeField,
    IntField,
    ListField,
    ReferenceField,
    StringField,
)
from flask_security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, auth_required, hash_password, permissions_accepted


class Role(Document, RoleMixin):
    db_name='mongo'
    name = StringField(max_length=80, unique=True)
    description = StringField(max_length=255)
    permissions = ListField(required=False)
    meta = {"db_alias": db_name}    