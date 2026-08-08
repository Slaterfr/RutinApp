from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash(password: str):
    """Hash password using Argon2"""
    return pwd_context.hash(password)

def verify(password, hashed_password):
    """Verify password against Argon2 hash"""
    return pwd_context.verify(password, hashed_password)