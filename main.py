# coding: utf-8

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse, JSONResponse
import sqlite3
from utils import *
from database_operations import *
from models import *


app = FastAPI()

security = HTTPBasic()


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("database.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()


@app.post('/user/register')
async def register(register_data: RegisterData):
    database_user = get_user(app, register_data.login)

    if database_user:
        return JSONResponse(status_code=406, content={"Error": "User already exists",
                                                      "username": register_data.login})

    token = generate_token()
    add_user(app, register_data.login, token)
    send_token_email(register_data, token)

    return JSONResponse(status_code=201, content={"Status": "User successfully created",
                                                  "username": register_data.login})


@app.post("/message/new")
async def new_message(message: Message, credentials: HTTPBasicCredentials = Depends(security)):
    login = credentials.username
    token = credentials.password

    if not authenticate_user(app, login, token):
        return JSONResponse(status_code=406, content={"Error": "User does not exist",
                                                      "username": login})

    add_message(app, login, message.content)
    database_message = get_last_message_for_user(app, login)
    return JSONResponse(status_code=201, content={"Status": "Message successfully created",
                                                  "message_id": database_message[0]})



@app.put('/message/edit/{message_id}')
async def edit_message(message_id, message: Message, credentials: HTTPBasicCredentials = Depends(security)):
    login = credentials.username
    token = credentials.password

    if not authenticate_user(app, login, token):
        return JSONResponse(status_code=406, content={"Error": "User does not exist",
                                                      "username": login})

    database_message = get_message(app, message_id)

    if not database_message:
        return JSONResponse(status_code=406, content={"Error": "ID message not found",
                                                      "message_id": message_id})

    if login != database_message[1]:
        return JSONResponse(status_code=406, content={"Error": "Cannot edit message",
                                                      "message_id": message_id})

    update_message(app, message_id, message.content, 0)

    return JSONResponse(content={"Status": "Message successfully edited",
                                 "message_id": message_id})


@app.delete('/message/delete/{message_id}')
async def delete_massage(message_id, credentials: HTTPBasicCredentials = Depends(security)):
    login = credentials.username
    token = credentials.password

    if not authenticate_user(app, login, token):
        return JSONResponse(status_code=406, content={"Error": "User does not exist",
                                                      "username": login})

    database_message = get_message(app, message_id)

    if not database_message:
        return JSONResponse(status_code=406, content={"Error": "Message not found",
                                                      "message_id": message_id})

    if login != database_message[1]:
        return JSONResponse(status_code=406, content={"Error": "Cannot delete message",
                                                      "message_id": message_id})

    delete_message(app, message_id)
    return JSONResponse(content={"Status": "Message successfully deleted",
                                 "message_id": message_id})


@app.get('/message/view/{message_id}')
async def view_message(message_id):
    database_message = get_message(app, message_id)
    if not database_message:
        return JSONResponse(status_code=406, content={"Error": "Message not found",
                                                      "message_id": message_id})

    message_content = database_message[2]
    message_counter = int(database_message[3]) + 1
    update_message(app, message_id, message_content, message_counter)

    return JSONResponse(content={
        "Author": database_message[1],
        "Counter": message_counter,
        "Content": message_content
    })
