# Notif.ai recruitment app - Kamil Pawlicki

## Description 
Recruitment app for Notifai that simulates simple blog

## Used technologies
* Python 3.8
* sqlite3
* fastapi
* uvicorn
* pytest

## Run app

Download source and requiremets.txt and in the terminal type in the root directory:

* basic

`uvicorn main:app`

* auto-reload:

`uvicorn main:app --reload`

* port

http://127.0.0.1:8000/

* docs

http://127.0.0.1:8000/docs

## Cloud

Api is available on heroku cloud:

https://notifai-recruitment-app.herokuapp.com/

API docs:

https://notifai-recruitment-app.herokuapp.com/docs

## Endpoints

* https://notifai-recruitment-app.herokuapp.com/user/register               Through that endpoint You can register new user
* https://notifai-recruitment-app.herokuapp.com/message/new                 Through that endpoint You can add new message 
* https://notifai-recruitment-app.herokuapp.com/message/edit/[message_id]   Through that endpoint You can edit message with given ID
* https://notifai-recruitment-app.herokuapp.com/message/delete/{message_id} Through that endpoint You can delete message with given ID
* https://notifai-recruitment-app.herokuapp.com/message/view/{message_id}   Through that endpoint You can view message with given ID

## Post data format

* https://notifai-recruitment-app.herokuapp.com/user/register 
```
curl -X 'POST' \
  'https://notifai-recruitment-app.herokuapp.com/user/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "login": "Your_login",
  "email": "Your_email@some_domain.com"
}'
```
* https://notifai-recruitment-app.herokuapp.com/message/new 
```
curl -X 'POST' \
  'https://notifai-recruitment-app.herokuapp.com/message/new' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic Login&Password=' \
  -H 'Content-Type: application/json' \
  -d '{
  "content": "Message text"
}'
```
* https://notifai-recruitment-app.herokuapp.com/message/edit/[message_id]

```
curl -X 'PUT' \
  'https://notifai-recruitment-app.herokuapp.com/message/edit/[message_id]' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic Login&Password=' \
  -H 'Content-Type: application/json' \
  -d '{
  "content": "Edit message text"
}'
```

* https://notifai-recruitment-app.herokuapp.com/message/delete/[message_id]

```
curl -X 'DELETE' \
  'https://notifai-recruitment-app.herokuapp.com/message/delete/[message_id]' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic Login&Password='
```

* https://notifai-recruitment-app.herokuapp.com/message/view/[message_id]

```

curl -X 'GET' \
  'https://notifai-recruitment-app.herokuapp.com/message/view/[message_id]' \
  -H 'accept: application/json'

```


## Response format
* Status contains response code that informs what happened 

```
{
        "status": status,
        "message": message,
        "value": value
}
```

### Possible Response status codes:

```
code_user_created = 1                   # User successfully created  
code_user_not_created = 2               # Wrong login or email
code_user_already_exists = 3            # User already exists
code_user_does_not_exist = 4            # User does not exist

code_message_created = 5                # Message successfully created
code_message_not_created = 6
code_message_not_found = 7              # Message not found

code_message_not_edited = 8             # Cannot edit message
code_message_edited = 9                 # Message successfully edited
code_message_deleted = 10               # Message successfully deleted
code_message_not_deleted = 11           # Cannot delete message

code_message_counter_update_error = 12  # Cannot update message view counter
```

## Response message view format  

```
{
        "Author": login,
        "Counter": message view counter,
        "Content": message content
}
```



