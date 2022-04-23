from .db import db


class Content(db.EmbeddedDocument):
    text = db.StringField()
    video = db.FileField()
    gif = db.FileField()


class Post(db.Document):
    id_user = db.StringField(required=True)
    date_create = db.DateTimeField()
    date_post = db.DateTimeField()
    name = db.StringField()
    password = db.StringField()
    email = db.StringField(unique=True, required=True)
    content = db.EmbeddedDocumentField(Content)


class PostDraft(db.Document):
    id_user = db.StringField(required=True)
    date_create = db.DateTimeField()
    date_post = db.DateTimeField()
    text = db.StringField()
    name = db.StringField()
    password = db.StringField()
    email = db.StringField(unique=True, required=True)
    content = db.EmbeddedDocumentField(Content)

