from pydantic import BaseModel, EmailStr


class UserSignUpSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr


class NameChangeSchema(BaseModel):
    name: str


class PasswordChangeSchema(BaseModel):
    password: str


class PostCreateSchema(BaseModel):
    title: str
    content: str


class PostUpdateSchema(BaseModel):
    title: str
    content: str


class UserCommentSchema(BaseModel):
    comment: str


class CommentChangeData(BaseModel):
    comment: str

