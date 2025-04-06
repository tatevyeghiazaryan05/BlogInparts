from fastapi import status, APIRouter, Depends
from fastapi.exceptions import HTTPException

from security import pwd_context, get_current_user

from schema import (
    NameChangeSchema,
    PasswordChangeSchema,
    UserOut,
    UserCommentSchema
)

# from main import mconn, cursor
import main


users_router = APIRouter(tags=["User API's"])


# ========================== User APIs ===================================


@users_router.get('/api/users')
def get_all_users(access_token=Depends(get_current_user)):
    try:
        main.cursor.execute("""SELECT * FROM users""")
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )

    try:
       all_users = main.cursor.fetchall()
       return all_users
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )


@users_router.get("/api/users/by-id/{id}", response_model=UserOut)
def get_user_by_id(id: int):
    try:
        main.cursor.execute("""SELECT * FROM users WHERE id=%s""",
                       (id,))
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )

    try:
        user = main.cursor.fetchone()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )

    return user


@users_router.get("/api/users/by-email/{email}", response_model=UserOut)
def get_user_by_email(email: str):
    try:
        main.cursor.execute("""SELECT * FROM users WHERE email = %s""",
                   (email,))
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )
    try:
        user = main.cursor.fetchone()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )
    return user


@users_router.put("/api/users/update/name")
def update_user_name(username_change_data: NameChangeSchema,
                     access_token=Depends(get_current_user)):

    user_id = dict(access_token).get("id")

    try:
        main.cursor.execute("""UPDATE users SET name = %s WHERE id = %s""",
                   (username_change_data.name, user_id))
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )
    try:
        main.conn.commit()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )
    return "Username updated successfully !!"


@users_router.put("/api/users/update/password")
def change_password(password_change_data: PasswordChangeSchema,
                     access_token=Depends(get_current_user)):

    user_id = dict(access_token).get("id")

    try:
        new_password = pwd_context.hash(password_change_data.password)
        main.cursor.execute("""UPDATE users SET password=%s WHERE id = %s """,
                   (new_password, user_id))
        main.conn.commit()
        return "Password updated successfully!!"
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )


@users_router.delete("/api/users/delete")
def delete_user(access_token=Depends(get_current_user)):

    user_id = dict(access_token).get("id")

    try:
        main.cursor.execute("""DELETE FROM users WHERE id = %s""",
                            (user_id,))
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )

    try:
        main.conn.commit()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )
    return "User was deleted"
