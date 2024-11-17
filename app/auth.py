from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from app import schemas, models, utils, database, email_service
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import os
from app.email_service import send_verification_email

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=dict)
def signup(user: schemas.UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = utils.hash_password(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    encrypted_url = utils.encrypt_url(user.email)

    verification_link = f"http://yourfrontend.com/verify/{encrypted_url}"
    send_verification_email(user.email, verification_link, background_tasks)

    return {"message": "User created, verification email sent", "encrypted_url": encrypted_url}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = utils.create_access_token({"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/upload")
def upload_file(file: UploadFile, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_data = utils.jwt.decode(token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
    if user_data["role"] != "Ops":
        raise HTTPException(status_code=403, detail="Only Ops users can upload files")

    if not file.filename.endswith((".pptx", ".docx", ".xlsx")):
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_path = f"./files/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    secure_url = utils.encrypt_url(file_path)
    new_file = models.File(filename=file.filename, owner_id=user_data["sub"], secure_url=secure_url)
    db.add(new_file)
    db.commit()
    return {"message": "File uploaded successfully"}

@router.get("/list-files", response_model=list[schemas.FileResponse])
def list_files(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_data = utils.jwt.decode(token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
    files = db.query(models.File).filter(models.File.owner_id == user_data["sub"]).all()
    return files

@router.get("/download/{file_id}")
def download_file(file_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_data = utils.jwt.decode(token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
    file = db.query(models.File).filter(models.File.id == file_id).first()

    if not file or file.owner_id != user_data["sub"]:
        raise HTTPException(status_code=403, detail="Access denied")

    decrypted_path = utils.decrypt_url(file.secure_url)
    return {"download-link": decrypted_path, "message": "success"}
