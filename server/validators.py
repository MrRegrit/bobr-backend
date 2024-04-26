import re


class Validator:
    @staticmethod
    def validate_email(email):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        return re.fullmatch(regex, email) and type(email) is str

    @staticmethod
    def validate_nick(nick):
        return (
            type(nick) is str
            and len(nick) > 3
            and "@" not in nick
            and nick[0].isalpha()
            and nick.isalnum()
        )

    @staticmethod
    def validate_password(password):
        if type(password) is str and 8 <= len(password) <= 20:
            count_num = 0
            count_alph = 0
            for i in password:
                if i.isalpha():
                    count_alph += 1
                    if i.lower() not in "abcdefghijklmnopqrstuvwxyz":
                        return False
                elif i.isdigit():
                    count_num += 1
            if count_alph >= 1 and count_num >= 1:
                return True
        return False

    @staticmethod
    def user_is_valid(email, nick, password):
        if not Validator.validate_email(email):
            return {"error": "Введите корректную почту"}
        if not Validator.validate_nick(nick):
            return {
                "error": "Ник должен быть от 3-х символов, не содержать @ и начинаться с буквы"
            }
        if not Validator.validate_password(password):
            return {
                "error": "Пароль должен быть от 8 до 20 символов и иметь хотябы одну букву или цифру"
            }
        return True

    @staticmethod
    def validate_title(title):
        return type(title) is str and 5 < len(title) < 200

    @staticmethod
    def validate_text(text):
        return type(text) is str and len(text) > 10

    @staticmethod
    def post_is_valid(title, text):
        if not Validator.validate_title(title):
            return {"error": "Название должно быть от 5-ти до 200-т символов"}
        if not Validator.validate_text(text):
            return {"error": "Пост должен быть от 10-ти символов"}
        return True
