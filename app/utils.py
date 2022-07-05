from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashing_password(password: str):
    return password_context.hash(password)
