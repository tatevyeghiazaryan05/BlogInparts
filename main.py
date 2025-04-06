import time

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from psycopg2.extras import RealDictCursor
import psycopg2
from database import engine
from models import Base

from users import users_router
from post import posts_router
from auth import users_auth_router
from comments import comment_router
from my_account import account_router


while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            user='postgres',
            password='password',
            database='blog',
            cursor_factory=RealDictCursor
        )

        cursor = conn.cursor()
        print("Database connection successfully...")
        break
    except Exception as err:
        print(err)
        time.sleep(2)


Base.metadata.create_all(bind=engine)


app = FastAPI()
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(users_auth_router)
app.include_router(users_router)
app.include_router(posts_router)
app.include_router(comment_router)
app.include_router(account_router)
