import flask
from flask_jwt_simple import create_jwt

from objects import User, Post, Comment


def make_resp(message, status):
    resp = flask.make_response(message, status)
    resp.headers["Content-type"] = "application/json; charset=utf-8"
    return resp


def check_keys(dct, keys):
    return all(key in dct for key in keys)


def create_jwt_generate_response(id, nick):
    j_token = {"token": create_jwt(identity={"id": id, "nick": nick})}
    return j_token


def create_class_post(*info):
    user = User(*info[:4])
    post = Post(*info[4:], user)
    return post


def create_class_comment(*info):
    user = User(*info[:4])
    comment = Comment(*info[4:], user)
    return comment
