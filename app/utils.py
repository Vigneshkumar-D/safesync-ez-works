from passlib.context import CryptContext
from jose import jwt
from cryptography.fernet import Fernet

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
encryption_key = Fernet.generate_key()
fernet = Fernet(encryption_key)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def decrypt_url(encrypted_url: str) -> str:
    return fernet.decrypt(encrypted_url.encode()).decode()

def encrypt_url(url: str) -> str:
    return fernet.encrypt(url.encode()).decode()
