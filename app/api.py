from flask import Flask, request, Response, jsonify
from flask_jwt_extended import JWTManager, create_access_token, \
                                jwt_required, get_jwt_identity
from app.database.db import initialize_db
from app.database.models import Post, PostDraft
#from flasgger import Swagger

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/post'
}

app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

initialize_db(app)
jwt = JWTManager(app)


@app.route('/posts', methods=['GET', 'POST'])
@jwt_required()
# получение всех постов и создание нового
def posts():
    get_jwt_identity()
    if request.method == 'GET':
        data = Post.objects()
        return data
    else:
        data = request.json()
        files = request.files('image')
        post = Post(**data).save
        return {"data": post, }


@app.route('/post/<post_id_>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
# получение редактирование, удаление поста по id
def post_id(post_id_):
    get_jwt_identity()
    post = Post.objects.get(id=post_id)
    if request.method == 'GET':
        return {"data": post_id_, "id": str(post['id'])}
    elif request.method == 'PUT':
        data = request.get_json()
        post.update_one(**data)
        post.save()
    else:
       Post.delete_many(post)


@app.route('/post_draft', methods=['GET', 'POST'])
@jwt_required()
# Получение и добавление в черновики
def draft():
    get_jwt_identity()
    if request.method == 'GET':
        draft = PostDraft.objects()
        return jsonify(draft)
    else:
        data = request.json()
        files = request.files('image')
        draft = PostDraft(**data).save
        return {"data": draft, }


@app.route('/post_draft/<draft_id_>', methods=['GET', 'PUT', 'DELET'])
@jwt_required()
def draft_id(draft_id_):
    get_jwt_identity()
    draft = PostDraft.objects.get(id=draft_id_)
    if request.method == 'GET':
        return {"data": draft, "id": str(draft['id'])}
    elif request.method == 'PUT':
        data = request.get_json()
        draft.update_one(**data)
        draft.save()
    else:
        Post.delete_many(draft)