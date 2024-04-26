CREATE TABLE Users
(
    id       SERIAL PRIMARY KEY,
    email    VARCHAR(40) NOT NULL UNIQUE,
    nick     VARCHAR(20) NOT NULL UNIQUE,
    password varchar(200) NOT NULL
);
CREATE TABLE Posts
(
    id       SERIAL PRIMARY KEY,
    datetime TIMESTAMP,
    text     TEXT,
    title   VARCHAR(200),
    user_id  INTEGER REFERENCES Users (id) ON DELETE CASCADE
);
CREATE TABLE Comments
(
    id       SERIAL PRIMARY KEY,
    text     TEXT,
    datetime TIMESTAMP,
    user_id  INTEGER REFERENCES Users (id) ON DELETE CASCADE,
    post_id  INTEGER REFERENCES Posts (id) ON DELETE CASCADE
);
CREATE TABLE Likes
(
    id      SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users (id) ON DELETE CASCADE,
    post_id INTEGER REFERENCES Posts (id) ON DELETE CASCADE
);
CREATE TABLE Dislikes
(
    id      SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users (id) ON DELETE CASCADE,
    post_id INTEGER REFERENCES Posts (id) ON DELETE CASCADE
);

INSERT INTO Users (email, nick, password)
VALUES ('renogaba@gmail.com', 'regrit', '1234');

INSERT INTO Posts (datetime, text, title, user_id)
VALUES ('2024-03-28 00:00:00', 'Это тестовый пост!', 'Тестовый заголовок', 1);

INSERT INTO Likes (user_id, post_id)
VALUES (1, 1);

INSERT INTO Comments (text, datetime, user_id, post_id)
VALUES ('Тестовый комментарий', '2024-03-29 00:00:00', 1, 1)