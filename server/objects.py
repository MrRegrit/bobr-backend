class User:
    def __init__(self, id=None, email=None, nick=None, hashed_password=None):
        self.id = id
        self.email = email
        self.nick = nick
        self.hashed_password = hashed_password

    def has_data(self):
        if self.id is None:
            return False
        return True


class Post:
    def __init__(
        self,
        id=None,
        datetime=None,
        text=None,
        header=None,
        percent_likes=None,
        likes=None,
        dislikes=None,
        author=None,
    ):
        self.id = id
        self.datetime = datetime
        self.text = text
        self.header = header
        self.author = author
        self.percent_likes = percent_likes
        self.likes = likes
        self.dislikes = dislikes

    def has_data(self):
        if self.id is None:
            return False
        return True

    def to_dict(self):
        if self.has_data():
            res = {
                "header": self.header,
                "text": self.text,
                "id": self.id,
                "datatime": self.datetime,
                "author": self.author.nick,
                "likes": self.likes,
                "dislikes": self.dislikes,
                "percent_likes": self.percent_likes,
            }
            return res
        return {}


class Comment:
    def __init__(self, id=None, text=None, datetime=None, author=None):
        self.id = id
        self.datetime = datetime
        self.text = text
        self.author = author

    def has_data(self):
        if self.id is None:
            return False
        return True

    def to_dict(self):
        if self.has_data():
            res = {
                "text": self.text,
                "id": self.id,
                "datatime": self.datetime,
                "author": self.author.nick,
            }
            return res
        return {}
