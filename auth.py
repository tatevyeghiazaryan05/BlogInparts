from fastapi import status, APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
from pydantic import EmailStr

from security import pwd_context, create_access_token

from schema import (
    UserLoginSchema
)

# from main import mconn, cursor
import main


users_auth_router = APIRouter(tags=["Auth API's"])

UPLOAD_DIRECTORY = Path("uploads")
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)


@users_auth_router.post("/api/users/auth/sign-up")
def sign_up(
    name: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    file: UploadFile = File(...),
):
    file_extension = file.filename.split('.')[-1].lower()
    valid_extensions = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'eps']

    if file_extension not in valid_extensions:
        return JSONResponse(
            content={"message": f"Invalid file type. Allowed types are: {', '.join(valid_extensions)}"},
            status_code=400
        )

    file_path = UPLOAD_DIRECTORY / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        hashed_password = pwd_context.hash(password)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred while trying to hash password\n"
                   f"ERR: {err}"
        )

    try:
        main.cursor.execute("""INSERT INTO users (name,email,password,image_name) VALUES (%s,%s,%s,%s)""",
                            (name, email, hashed_password, file.filename))
        main.conn.commit()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred while trying to store data into database\n"
                   f"ERR: {err}"
        )

    return "Sign Up Successfully!!"


@users_auth_router.post("/api/users/auth/login")
def login(user_login_data: UserLoginSchema):
    try:
        email = user_login_data.email
        password = user_login_data.password
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred while trying to get given log in data\n"
                   f"ERR: {err}"
        )

    try:
        main.cursor.execute("""SELECT * FROM users WHERE email=%s""",
                        (email,))

        user = main.cursor.fetchone()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred while trying to store data into database\n"
                   f"ERR: {err}"
        )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email '{email}' was not found!"
        )

    user = dict(user)
    password_hash_from_db = user.get('password')

    if not pwd_context.verify(password, password_hash_from_db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Wrong password -> '{password}'"
        )

    user_info = {
        "id": user.get("id"),
    }

    access_token = create_access_token(user_info)

    image_filename = user.get("image_name")
    image_url = f"http://localhost:8000/uploads/{image_filename}"

    response_data = {
        "access_token": access_token,
        "token_type": "Bearer",
        "image": image_url

    }

    return response_data
