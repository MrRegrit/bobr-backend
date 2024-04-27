import jwt

from flask_jwt_simple import JWTManager
from flask_jwt_simple.config import config


class MyJWTManager(JWTManager):
    def _create_jwt(self, identity):
        jwt_data = self._get_jwt_data(identity)
        secret = config.encode_key
        algorithm = config.algorithm
        return jwt.encode(jwt_data, secret, algorithm)