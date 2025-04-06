from fastapi import status, APIRouter, Depends
from fastapi.exceptions import HTTPException

from schema import UserCommentSchema, CommentChangeData
from security import get_current_user

import main
comment_router = APIRouter(tags=["Comment API's"])


@comment_router.post("/api/users/comment/{post_id}")
def add_comment(post_id: int, user_comment_data: UserCommentSchema, access_token=Depends(get_current_user)):
    user_id = dict(access_token).get("id")
    try:
       comment = user_comment_data.comment

    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred while trying to get given log in data\n"
                   f"ERR: {err}"
        )
    try:
        main.cursor.execute("""INSERT INTO comments (comment,post_id,user_id) VALUES (%s,%s,%s)""",
                            (comment, post_id, user_id))
        main.conn.commit()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )

    return "Commented successfully"



from fastapi import status, APIRouter, Depends
from fastapi.exceptions import HTTPException
from security import get_current_user
import main

comment_router = APIRouter(tags=["Comment API's"])


@comment_router.delete("/api/users/comment/{comment_id}")
def delete_comment(comment_id: int, access_token=Depends(get_current_user)):
    user_id = dict(access_token).get("id")

    try:
        main.cursor.execute("""SELECT * FROM comments WHERE id = %s""", (comment_id,))
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking comment: {str(err)}"
        )

    comment = main.cursor.fetchone()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    post_id = comment['post_id']

    try:
        main.cursor.execute("""SELECT user_id FROM posts WHERE id = %s""", (post_id,))
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking post owner: {str(err)}"
        )

    post = main.cursor.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    post_user_id = post['user_id']

    if user_id != comment['user_id'] and user_id != post_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this comment"
        )
    try:
        main.cursor.execute("""DELETE FROM comments WHERE id = %s""", (comment_id,))
        main.conn.commit()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting comment: {str(err)}"
        )

    return {"message": "Comment deleted successfully!"}


from fastapi import status, APIRouter, Depends
from fastapi.exceptions import HTTPException
from schema import CommentChangeData  # Assuming CommentChangeData schema is defined
from security import get_current_user
import main

comment_router = APIRouter(tags=["Comment API's"])


@comment_router.put("/api/users/comment/change/{comment_id}")
def update_comment(comment_id: int, comment_change_data: CommentChangeData, access_token=Depends(get_current_user)):
    user_id = dict(access_token).get("id")
    try:
        main.cursor.execute("""SELECT * FROM comments WHERE id = %s""", (comment_id,))
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking comment: {str(err)}"
        )

    comment = main.cursor.fetchone()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    if comment['user_id'] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to edit this comment"
        )

    try:
        main.cursor.execute("""UPDATE comments SET comment = %s WHERE id = %s""",
                             (comment_change_data.comment, comment_id))
        main.conn.commit()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating comment: {str(err)}"
        )

    return {"message": "Comment updated successfully!"}
