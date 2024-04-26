from datetime import timedelta

from flask import Flask, g, request, jsonify
from flask_jwt_simple import JWTManager, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from db_code import FlaskDB, get_db
from misc import make_resp, check_keys, create_jwt_generate_response
from validators import Validator

app = Flask(__name__)
app.config["SECRET_KEY"] = "!!!"
app.config["JWT_SECRET_KEY"] = "top_sicret"
app.config["JWT_EXPIRES"] = timedelta(hours=24)
app.config["JWT_IDENTITY_CLAIM"] = "user"
app.config["JWT_HEADER_NAME"] = "authorization"
app.jwt = JWTManager(app)

postgres: FlaskDB = None


@app.before_request
def before_request():
    global postgres

    db = get_db()
    postgres = FlaskDB(db)


@app.teardown_request
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()


@app.post("/api/registration/")
def registration():
    data = request.get_json()
    if not data:
        return make_resp(jsonify({"error": "Empty request"}), 400)
    if not check_keys(data, ("email", "nick", "password")):
        return make_resp(jsonify({"error": "Bad request"}), 400)

    email = data["email"]
    nick = data["nick"]
    password = data["password"]

    user_is_validated = Validator.user_is_valid(email, nick, password)

    if user_is_validated is True:
        hashed_password = generate_password_hash(password)
        created_user = postgres.create_user(email, nick, hashed_password)
        if "error" in created_user:
            return make_resp(jsonify(created_user), 200)
        else:
            return make_resp(
                jsonify(
                    create_jwt_generate_response(created_user["id"], nick)
                ),
                200,
            )
    return make_resp(jsonify(user_is_validated), 200)


@app.post("/api/login/")
def user_login():
    data = request.get_json()
    if not data:
        return make_resp(jsonify({"error": "Empty request"}), 400)
    if not check_keys(data, ("login", "password")):
        return make_resp(jsonify({"error": "Bad request"}), 400)

    login = data["login"]
    password = data["password"]

    user = postgres.get_user(login)
    if not user.has_data() or not check_password_hash(
        user.hashed_password, password
    ):
        return make_resp(
            jsonify({"error": "Введите правильный логин и пароль"}), 200
        )
    return make_resp(
        jsonify(create_jwt_generate_response(user.id, user.nick)), 200
    )


@app.get("/api/post/<int:id>/")
def post(id):
    return make_resp(jsonify(postgres.get_post(id).to_dict()), 200)


@app.get("/api/new_posts/")
def new_posts():
    posts = postgres.get_new_posts()
    return make_resp(jsonify([post.to_dict() for post in posts]), 200)


@app.get("/api/popular_posts/")
def popular_post():
    posts = postgres.get_popular_posts()
    return make_resp(jsonify([post.to_dict() for post in posts]), 200)


@app.post("/api/posts/")
@jwt_required
def create_post():
    data = request.get_json()
    if not data:
        return make_resp(jsonify({"error": "Empty request"}), 400)
    if not check_keys(data, ("text", "title")):
        return make_resp(jsonify({"error": "Bad request"}), 400)

    title = data["title"]
    text = data["text"]

    post_is_validated = Validator.post_is_valid(title, text)

    if post_is_validated is True:
        user_id = get_jwt_identity()["id"]
        created_post = postgres.create_post(title, text, user_id)
        if "error" in created_post:
            return make_resp(jsonify(created_post), 400)
        else:
            return make_resp(jsonify(created_post), 200)

    return make_resp(jsonify(post_is_validated), 200)


@app.delete("/api/post/<int:id>/")
@jwt_required
def delete_post(id):
    user_id = get_jwt_identity()["id"]
    deleted_post = postgres.delete_post(id, user_id)
    if "error" in deleted_post:
        return make_resp(jsonify(deleted_post), 400)
    return make_resp(jsonify(deleted_post), 200)


@app.get("/api/profile/<string:nick>/")
def profile(nick):
    posts = postgres.get_profile(nick)
    return make_resp(jsonify([post.to_dict() for post in posts]), 200)


@app.get("/api/post/<int:post_id>/comments/")
def comments(post_id):
    comms = postgres.get_comments(post_id)
    return make_resp(
        jsonify([comment.to_dict() for comment in comms]), status=1
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
