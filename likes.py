from fastapi import status, APIRouter, Depends
from fastapi.exceptions import HTTPException

from security import get_current_user


like_router = APIRouter(tags=["Comment API's"])


@like_router.post("/api/users/like/{post_id}")
def add_comment(post_id: int, access_token=Depends(get_current_user)):
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

    try:
        main.cursor.execute("""SELECT * FROM likes WHERE post_id = %s AND user_id = %s""",
                            (post_id, user_id))
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking like status: {str(err)}"
        )

    like = main.cursor.fetchone()

    if like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already liked this post"
        )

    try:
        main.cursor.execute("""INSERT INTO likes (post_id, user_id, likes) VALUES (%s, %s)""",
                            (post_id, user_id, 1))
        main.conn.commit()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding like: {str(err)}"
        )

    try:
        main.cursor.execute("""UPDATE likes SET likes = likes + 1 WHERE post_id = %s AND user_id = %s""",
                             (post_id, user_id))

        main.conn.commit()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating post likes: {str(err)}"
        )

    return {"message": "Post liked successfully!"}


from fastapi import status, APIRouter, Depends
from fastapi.exceptions import HTTPException
from security import get_current_user
import main

like_router = APIRouter(tags=["Like API's"])


@like_router.post("/api/users/unlike/{post_id}")
def unlike_post(post_id: int, access_token=Depends(get_current_user)):
    user_id = dict(access_token).get("id")

    try:
        main.cursor.execute("""SELECT * FROM posts WHERE id = %s """, (post_id,))
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )

    post = main.cursor.fetchone()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    try:
        main.cursor.execute("""SELECT * FROM likes WHERE post_id = %s AND user_id = %s""",
                            (post_id, user_id))
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking like status: {str(err)}"
        )

    like = main.cursor.fetchone()

    if not like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have not liked this post"
        )

    try:
        main.cursor.execute("""DELETE FROM likes WHERE post_id = %s AND user_id = %s""",
                            (post_id, user_id))
        main.conn.commit()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error removing like: {str(err)}"
        )

    try:
        main.cursor.execute("""UPDATE posts SET likes = likes - 1 WHERE id = %s""", (post_id,))
        main.conn.commit()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating post likes: {str(err)}"
        )

    return {"message": "Post unliked successfully!"}
