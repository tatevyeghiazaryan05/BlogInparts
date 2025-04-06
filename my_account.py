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


account_router = APIRouter(tags=["Auth API's"])

UPLOAD_DIRECTORY = Path("uploads")
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)


@account_router.post("/api/users/auth/sign-up")
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