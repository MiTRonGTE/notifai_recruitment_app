def add_user(app, login, token):
    app.db_connection.execute(f"""INSERT INTO User (Login, Token) VALUES ('{login}', '{token}')""")
    app.db_connection.commit()


def get_user(app, login):
    return app.db_connection.execute(f"SELECT * FROM User WHERE Login = '{login}'").fetchone()


def authenticate_user(app, login, token):
    user = app.db_connection.execute(f"SELECT * FROM User WHERE Login = '{login}' and Token = '{token}'").fetchone()
    return bool(user)


def add_message(app, login, content):
    app.db_connection.execute(f"INSERT INTO Message (UserLogin, Content, Counter) VALUES ('{login}', '{content}', 0)")
    app.db_connection.commit()


def get_message(app, message_id):
    return app.db_connection.execute("SELECT * FROM Message WHERE MessageID = ?", (message_id,)).fetchone()


def get_last_message_for_user(app, login):
    return app.db_connection.execute(f"SELECT * FROM Message WHERE UserLogin = '{login}' ORDER BY MessageID DESC").fetchone()


def update_message(app, message_id, content, counter):
    app.db_connection.execute(f"UPDATE Message SET Content = '{content}', Counter = ? WHERE MessageID = ?",
                              (counter, message_id))
    app.db_connection.commit()


def delete_message(app, message_id):
    app.db_connection.execute("DELETE FROM Message WHERE MessageID = ?", (message_id, ))
    app.db_connection.commit()
