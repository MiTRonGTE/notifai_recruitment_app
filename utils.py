from random import randint
import hashlib
import smtplib
import ssl
from models import RegisterData
import re


def generate_token():
    return hashlib.sha256(f"{randint(0,10000000000)}{randint(0,10000000000)}".encode()).hexdigest()


def try_email(email):
    regex = r'^(\w|.||-)+[@](\w||-|.)+[.]\w{2,3}$'
    return re.search(regex, email)


def create_json_response(status, message, value):
    return {
        "status": status,
        "message": message,
        "value": value
    }


def send_token_email(register_data: RegisterData, token):
    server_name = "smtp.gmail.com"
    port = 465
    context = ssl.create_default_context()
    from_address = "notifai.recruitment.app.kp@gmail.com"
    password = "Not$o$ecurePa$$"
    body = f"""\
Subject: Your token for Notif.ai Recruitment App KP
    
Hello there, [ {register_data.login} ]!
here is your login token:
    
{token}"""

    with smtplib.SMTP_SSL(server_name, port, context=context) as server:
        server.login(from_address, password)
        server.sendmail(
            from_address,
            register_data.email,
            body)
