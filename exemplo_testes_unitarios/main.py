from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
from projeto import *
import pymysql
import json
import re

class User(BaseModel):
    fullName: str
    email: str
    city: str

class Like(BaseModel):
    idUser: str
    idPost: str
    like: bool

class Post(BaseModel):
    title: str
    postText: str
    urlPhoto: str
    idUser: str

with open('config_tests.json', 'r') as f:
    config = json.load(f)

connection = pymysql.connect(
    host=config['HOST'],
    user=config['USER'],
    password=config['PASS'],
    database='socialNetwork'
)

with connection.cursor() as cursor:
    cursor.execute('START TRANSACTION')
    cursor.execute('SET autocommit = 1')


app = FastAPI()

@app.get("/")
async def root():
    return {"msg": "Hello World"}

@app.get("/user/{fullName}")
async def find_user(fullName: str):
    idUser = acha_usuario(connection, fullName)
    return {"idUser": idUser, "fullName": fullName}

@app.post("/user/like/")
async def post_like(like: Like):
    try:
        adiciona_curtida(connection, like.idPost, like.idUser)
    except:
        pass

    if like.like:
        muda_para_pos(connection, like.idPost, like.idUser)
    elif not like.like:
        muda_para_neg(connection, like.idPost, like.idUser)
    return {"msg": "Like posted"}

@app.post("/user/")
async def create_user(user: User):
    adiciona_usuario(connection, user.fullName, user.email, user.city)
    return {"msg": "User Created"}

@app.post("/post/")
async def create_post(post: Post):
    adiciona_post(connection, post.title, post.postText, post.urlPhoto, post.idUser)

    birds = re.findall(r"#(\w+)", post.postText)
    users = re.findall(r"@(\w+)", post.postText)

    if len(birds) > 0:
        print(birds)
        idPost = acha_post(connection, post.title)
        for bird in birds:
            idBird = acha_passaro(connection, bird)
            adiciona_tag(connection, idPost, idBird)

    if len(users) > 0:
        print(users)
        idPost = acha_post(connection, post.title)
        for user in users:
            idUser = acha_usuario(connection, user)
            adiciona_mencao(connection, idPost, idUser)

    return {"msg": "Post posted"}

@app.delete("/post/{idPost}")
async def delete_post(idPost: str):
    remove_post(connection, idPost)
    return {"msg": "Post removed"}

@app.get("/user/posts/{idUser}")
async def get_user_posts(idUser: str):
    res = lista_novos(connection, idUser)
    return res

@app.get("/user/popular")
async def get_popular_users():
    res = lista_populares(connection)
    return res
