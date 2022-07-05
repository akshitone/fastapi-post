from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashing_password(password: str):
    return password_context.hash(password)


def verify_password(user_password: str, hashed_password: str):
    return password_context.verify(user_password, hashed_password)
