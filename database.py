from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


# URL -> Uniform Resource Locator
# protocol://username:password@host:port/path/to/resource?p1=v1&p2=v2&p3=v3
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/blog"

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base = declarative_base()
except Exception as err:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(err)
    )
