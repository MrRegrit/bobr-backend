from datetime import datetime

import psycopg2
import psycopg2.errors
import flask

from objects import User
from misc import create_class_post, create_class_comment
import sql_requests


def connect():
    conn = psycopg2.connect(
        host="postgres",
        database="postgres",
        user="regrit",
        password="123",
    )
    return conn


def get_db():
    if not hasattr(flask.g, "link_db"):
        flask.g.ling_db = connect()
    return flask.g.ling_db


class FlaskDB:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def create_user(self, email, nick, password):
        try:
            sql = sql_requests.create_user.format(
                email=email, nick=nick, password=password
            )
            self.__cur.execute(sql)
            self.__db.commit()
            user_id = self.__cur.fetchone()[0]
            return {"id": user_id}
        except psycopg2.errors.UniqueViolation as exp:
            if "Key (email)" in str(exp):
                return {"error": "Пользователь с такой почтой уже существует"}
            if "Key (nick)" in str(exp):
                return {"error": "Пользователь с таким ником уже существует"}
        except Exception as exp:
            return {"error": str(exp)}

    def get_user(self, value):
        """can search user with id, nick or email"""
        search = "nick"
        if value.isdigit():
            search = "id"
        elif "@" in value:
            search = "email"
        sql = sql_requests.get_user.format(search=search, value=value)
        self.__cur.execute(sql)
        res = self.__cur.fetchone()
        if res:
            return User(*res)
        return User()

    def get_posts(self, sql):
        try:
            self.__cur.execute(sql)
            posts = [
                create_class_post(*post) for post in self.__cur.fetchall()
            ]
            return posts
        except Exception as exp:
            return []

    def get_popular_posts(self):
        sql = sql_requests.get_popular_posts
        return self.get_posts(sql)

    def get_new_posts(self):
        sql = sql_requests.get_new_posts
        return self.get_posts(sql)

    def get_post(self, id):
        sql = sql_requests.get_post.format(id=id)
        post = self.get_posts(sql)
        if post:
            return post[0]
        return {}

    def create_post(self, title, text, user_id):
        try:
            now = datetime.now()
            sql = sql_requests.create_post.format(
                datetime=now, text=text, title=title, user_id=user_id
            )
            self.__cur.execute(sql)
            self.__db.commit()
            post_id = self.__cur.fetchone()[0]
            return {"id": post_id}
        except Exception as exp:
            return {"error": str(exp)}

    def delete_post(self, id, user_id):
        try:
            sql = sql_requests.delete_post.format(id=id, user_id=user_id)
            self.__cur.execute(sql)
            self.__db.commit()
            post_id = self.__cur.fetchone()
            if post_id:
                return {post_id[0]: "deleted"}
            else:
                return {"error": "Поста не существует или вы не его создатель"}
        except Exception as exp:
            return {"error": str(exp)}

    def get_profile(self, nick):
        try:
            sql = sql_requests.get_profile.format(nick=nick)
            self.__cur.execute(sql)
            posts = [
                create_class_post(*post) for post in self.__cur.fetchall()
            ]
            return posts
        except Exception as exp:
            return []

    def get_comments(self, post_id):
        try:
            sql = sql_requests.get_comments.format(post_id=post_id)
            self.__cur.execute(sql)
            comments = [
                create_class_comment(*comment)
                for comment in self.__cur.fetchall()
            ]
            return comments
        except Exception as exp:
            return []
