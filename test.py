import sqlite3

from fastapi.security import HTTPBasic
from requests.auth import HTTPBasicAuth
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)
client.message1 = ''
client.message2 = ''


security = HTTPBasic()

app.db_connection = sqlite3.connect("database_test.db")
app.db_connection.execute("""DELETE FROM User""")
app.db_connection.execute("""DELETE FROM Message""")
app.db_connection.commit()


app.db_connection.execute("""INSERT INTO User (Login, Token) 
VALUES ('test1', 'bc79d55791381f6744a68f07a7984d098a5fffdc852a4e9eb57fcceb0a759f55')""")
app.db_connection.execute("""INSERT INTO User (Login, Token) 
VALUES ('test2', 'e4dc50a97d0542b78b5b39288fd3a8b85cabf38c4ea72c4c74126bfe187bb360')""")
app.db_connection.commit()


auth1 = HTTPBasicAuth(username="test1", password="bc79d55791381f6744a68f07a7984d098a5fffdc852a4e9eb57fcceb0a759f55")
auth2 = HTTPBasicAuth(username="test2", password="e4dc50a97d0542b78b5b39288fd3a8b85cabf38c4ea72c4c74126bfe187bb360")
auth3 = HTTPBasicAuth(username="test2", password="testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttest")
auth4 = HTTPBasicAuth(username="badlogin", password="e4dc50a97d0542b78b5b39288fd3a8b85cabf38c4ea72c4c74126bfe187bb360")


def test_new_message():
    # Poprawne utworzenie 1 wiedomości testowej
    response = client.post("/message/new", json={"content": "test message 1"}, auth=auth1)
    assert response.status_code == 201
    client.message1 = response.json()

    # Poprawne utworzenie 2 wiadomości testowej
    response = client.post("/message/new", json={"content": "test message 1"}, auth=auth2)
    assert response.status_code == 201
    client.message2 = response.json()

    # Pusta wiadomość
    response = client.post("/message/new", json={"content": ""}, auth=auth1)
    assert response.status_code == 422

    # Błędny token
    response = client.post("/message/new", json={"content": "test message 1"}, auth=auth3)
    assert response.status_code == 406

    # Brak użytkowniak w bazie danych
    response = client.post("/message/new", json={"content": "test message 1"}, auth=auth4)
    assert response.status_code == 406


def test_edit_message():
    # Poprawne edytowanie 1 wiadomości testowej
    response = client.put(f"/message/edit/{client.message1['message_id']}", json={"content": "test edit 1"},
                          auth=auth1)
    assert response.status_code == 200

    # Poprawne edytowanie 2 wiadomości testowej
    response = client.put(f"/message/edit/{client.message2['message_id']}", json={"content": "test edit 1"},
                          auth=auth2)
    assert response.status_code == 200

    # Brak wiadomości o wskazanym ID
    response = client.put(f"/message/edit/99999", json={"content": "test edit 1"},
                          auth=auth1)
    assert response.status_code == 406

    # Błędny token
    response = client.put(f"/message/edit/{client.message1['message_id']}", json={"content": "test edit 1"},
                          auth=auth3)
    assert response.status_code == 406

    # Brak użytkowniak w bazie danych
    response = client.put(f"/message/edit/{client.message1['message_id']}", json={"content": "test edit 1"},
                          auth=auth4)
    assert response.status_code == 406


def test_view_message():
    # poprawne wyświetlenie wiadomości
    response = client.get(f"/message/view/{client.message1['message_id']}")
    assert response.status_code == 200
    assert response.json() == {
        "Author": "test1",
        "Counter": 1,
        "Content": "test edit 1"}

    # poprawne wyświetlenie wiadomości testowanie zwiększania licznika
    response = client.get(f"/message/view/{client.message1['message_id']}")
    assert response.status_code == 200
    assert response.json() == {
        "Author": "test1",
        "Counter": 2,
        "Content": "test edit 1"}

    # poprawne wyświetlenie wiadomości testowanie resetowania licznika
    response = client.put(f"/message/edit/{client.message1['message_id']}", json={"content": "test edit 2"},
                          auth=auth1)
    assert response.status_code == 200

    # poprawne wyświetlenie wiadomości testowanie zwiększania licznika
    response = client.get(f"/message/view/{client.message1['message_id']}")
    assert response.status_code == 200
    assert response.json() == {
        "Author": "test1",
        "Counter": 1,
        "Content": "test edit 2"}

    # poprawne wyświetlenie wiadomości
    response = client.get(f"/message/view/{client.message2['message_id']}")
    assert response.status_code == 200

    # Poprawne usunięcie 2 wiadomości testowe
    response = client.delete(f"/message/delete/{client.message2['message_id']}", auth=auth2)
    assert response.status_code == 200

    # Brak wiadomości o danym ID
    response = client.get(f"/message/view/{client.message2['message_id']}")
    assert response.status_code == 406


def test_delete_message():
    # Brak wiadomości o wskazanym ID
    response = client.delete(f"/message/delete/9999999", auth=auth1)
    assert response.status_code == 406

    # Brak użytkowniak w bazie danych
    response = client.delete(f"/message/delete/{client.message1['message_id']}", auth=auth4)
    assert response.status_code == 406

    # Błędny token
    response = client.delete(f"/message/delete/{client.message1['message_id']}", auth=auth3)
    assert response.status_code == 406

    # Poprawne usunięcie 1 wiadomości testowe
    response = client.delete(f"/message/delete/{client.message1['message_id']}", auth=auth1)
    assert response.status_code == 200

