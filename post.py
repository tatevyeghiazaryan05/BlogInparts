from fastapi import status, APIRouter, Depends
from fastapi.exceptions import HTTPException

from models import Post
from schema import PostCreateSchema, PostUpdateSchema

from security import pwd_context, get_current_user


import main


posts_router = APIRouter(tags=["Post API's"])
# # ========================== Post APIs ===================================
# # CRUD -> Create, Read, Update, Delete


@posts_router.post("/api/posts")
def create_post(post_create_data: PostCreateSchema, access_token=Depends(get_current_user)):
    user_id = dict(access_token).get("id")

    try:
        title = post_create_data.title
        content = post_create_data.content
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )

    try:
        main.cursor.execute("""INSERT INTO posts (title, content, user_id )
                      VALUES(%s, %s, %s)""",
                   (title, content, user_id))
        main.conn.commit()
        return "Posted successfully!!"
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )


@posts_router.get("/api/posts")
def get_all_posts():
    try:
        main.cursor.execute("""SELECT * FROM posts""")
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )
    try:
        all_posts = main.cursor.fetchall()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )
    return all_posts


@posts_router.get("/api/posts/by-id/{id}")
def get_post_by_id(id: int):
    try:
        main.cursor.execute("""SELECT * FROM posts WHERE id=%s""",
                   (id,))
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )

    try:
        post = main.cursor.fetchone()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post was not found"
        )

    return post


@posts_router.get("/api/posts/by-user_id/{user_id}")
def get_post_by_user_id(user_id: int):
    try:
        main.cursor.execute("""SELECT * FROM posts WHERE user_id = %s """,
                   (user_id,))
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )

    try:
        post = main.cursor.fetchone()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post was not found"
        )

    return post


@posts_router.put("/api/posts/update/{post_id}")
def update_post(post_id: int, post_update_data: PostUpdateSchema, access_token=Depends(get_current_user)):
    user_id = dict(access_token).get("id")

    try:
        main.cursor.execute("""SELECT * FROM posts WHERE id = %s """,
                            (post_id,))
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )

    try:
        post = main.cursor.fetchone()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post was not found"
        )
    print(f"user_id who wants do update:{user_id}")
    print(f"Post User :{post['user_id']}")
    if user_id == post["user_id"]:
        try:
            title = post_update_data.title
            content = post_update_data.content
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error occurred while trying to get given update data\n"
                       f"ERR: {err}"
            )
        try:
            main.cursor.execute("""UPDATE posts SET title=%s, content = %s WHERE id = %s """,
                       (title, content, post_id))
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
        return "Post updated successfully!!"
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="It's not your post!!"
        )


@posts_router.delete("/api/posts/delete/{id}")
def delete_post(id: int):
    try:
        main.cursor.execute("""DELETE FROM posts WHERE id = %s""",
                   (id,))
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
    return "Post deleted successfully!!"
