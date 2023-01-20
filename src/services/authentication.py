import bcrypt
from passlib.context import CryptContext
from database.models import User

password_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

class Authentication(BaseException):
    pass

class AuthorizeService:
    def create_hashed_password(self, *,password):
        salt=self.generate_salt()
        hassed_password=self.hashed_password()

    def generate_salt(self):
        pass

    def hashed_password(self):
        pass