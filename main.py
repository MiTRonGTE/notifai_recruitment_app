# coding: utf-8

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
import sqlite3
from utils import *
from database_operations import *
from models import *
from constants import *


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
    if not try_email(register_data.email):
        return JSONResponse(status_code=406, content={})
    database_user = get_user(app, register_data.login)

    if database_user:
        return JSONResponse(status_code=406, content=create_json_response(code_user_already_exists, "User already exists!", register_data.login))
    token = generate_token()
    try:
        add_user(app, register_data.login, token)
    except Exception as ex:
        return JSONResponse(status_code=500, content=create_json_response(code_user_not_created, ex, None))

    send_token_email(register_data, token)

    return JSONResponse(status_code=201, content=create_json_response(code_user_created, "User successfully created!", register_data.login))


@app.post("/message/new")
async def new_message(message: Message, credentials: HTTPBasicCredentials = Depends(security)):
    login = credentials.username
    token = credentials.password

    if not authenticate_user(app, login, token):
        return JSONResponse(status_code=406, content=create_json_response(code_user_does_not_exist, "User does not exist!", login))
    try:
        add_message(app, login, message.content)
    except Exception as ex:
        return JSONResponse(status_code=500, content=create_json_response(code_message_not_created, ex, None))
    database_message = get_last_message_for_user(app, login)
    return JSONResponse(status_code=201, content=create_json_response(code_message_created, "Message successfully created!", database_message[0]))


@app.put('/message/edit/{message_id}')
async def edit_message(message_id, message: Message, credentials: HTTPBasicCredentials = Depends(security)):
    login = credentials.username
    token = credentials.password

    if not authenticate_user(app, login, token):
        return JSONResponse(status_code=406, content=create_json_response(code_user_does_not_exist, "User does not exist!", login))

    database_message = get_message(app, message_id)

    if not database_message:
        return JSONResponse(status_code=406, content=create_json_response(code_message_not_found, "Message not found!", message_id))

    if login != database_message[1]:
        return JSONResponse(status_code=406, content=create_json_response(code_message_not_edited, "Cannot edit message! Wrong authentication!", message_id))

    try:
        update_message(app, message_id, message.content, 0)
    except Exception as ex:
        return JSONResponse(status_code=500, content=create_json_response(code_message_not_edited, ex, message_id))

    return JSONResponse(content=create_json_response(code_message_edited, "Message successfully edited!", message_id))


@app.delete('/message/delete/{message_id}')
async def delete_massage(message_id, credentials: HTTPBasicCredentials = Depends(security)):
    login = credentials.username
    token = credentials.password

    if not authenticate_user(app, login, token):
        return JSONResponse(status_code=406,
                            content=create_json_response(code_user_does_not_exist, "User does not exist!", login))

    database_message = get_message(app, message_id)

    if not database_message:
        return JSONResponse(status_code=406, content=create_json_response(code_message_not_found, "Message not found!", message_id))

    if login != database_message[1]:
        return JSONResponse(status_code=406, content=create_json_response(code_message_not_deleted, "Cannot delete message! Wrong authentication!", message_id))

    try:
        delete_message(app, message_id)
    except Exception as ex:
        return JSONResponse(status_code=500, content=create_json_response(code_message_not_deleted, ex, message_id))

    return JSONResponse(content=create_json_response(code_message_deleted, "Message successfully deleted!", message_id))


@app.get('/message/view/{message_id}')
async def view_message(message_id):
    database_message = get_message(app, message_id)
    if not database_message:
        return JSONResponse(status_code=406, content=create_json_response(code_message_not_found, "Message not found!", message_id))

    message_content = database_message[2]
    message_counter = int(database_message[3]) + 1

    try:
        update_message(app, message_id, message_content, message_counter)
    except Exception as ex:
        return JSONResponse(status_code=500, content=create_json_response(code_message_counter_update_error, ex, message_id))

    return JSONResponse(content={
        "Author": database_message[1],
        "Counter": message_counter,
        "Content": message_content
    })
