base_get_post = """SELECT users.id,
       email,
       nick,
       password,
       posts.id,
       datetime,
       text,
       title,
       round(CASE
            WHEN pl.count_like > 0
                THEN (pl.count_like * 1.0 / (pdl.count_dislikes + pl.count_like) * 100)
            ELSE 0 END) as procent_like,
       pl.count_like,
       pdl.count_dislikes
FROM posts
         JOIN users ON users.id = posts.user_id
         JOIN (SELECT posts.id, count(l.user_id) as count_like
               FROM posts
                        LEFT JOIN likes l on posts.id = l.post_id
               GROUP BY posts.id) as pl ON pl.id = posts.id
         JOIN (SELECT posts.id, count(d.user_id) as count_dislikes
               FROM posts
                        LEFT JOIN dislikes d on posts.id = d.post_id
               GROUP BY posts.id) as pdl ON pdl.id = posts.id """

get_popular_posts = (
    base_get_post
    + """ORDER BY procent_like DESC, datetime DESC
LIMIT 10"""
)

get_new_posts = base_get_post + """ORDER BY datetime DESC LIMIT 10"""

get_post = base_get_post + """WHERE posts.id = '{id}'"""

create_user = """INSERT INTO users (email, nick, password)
VALUES ('{email}', '{nick}', '{password}') RETURNING id"""

create_post = """INSERT INTO posts (datetime, text, title, user_id) 
VALUES ('{datetime}', '{text}', '{title}', '{user_id}') RETURNING id"""

get_user = (
    "SELECT id, email, nick, password FROM users WHERE {search} = '{value}'"
)

delete_post = """DELETE FROM posts WHERE id = '{id}' and user_id = '{user_id}' RETURNING id"""

get_profile = (
    base_get_post + """WHERE nick = '{nick}' ORDER BY datetime DESC"""
)

get_comments = """SELECT users.id, users.email, users.nick, users.password, comments.id, text, datetime
FROM comments JOIN users on users.id = comments.user_id WHERE post_id = '{post_id}'"""
