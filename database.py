import os
import sqlite3

path_to_database = os.getcwd() + "/database.db"

class Database:
    def execute(self, request: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        data = None
        if parameters is None:
            parameters = tuple()
        with sqlite3.connect(path_to_database) as db:
            sql = db.cursor()
            sql.execute(request, parameters)
            if commit:
                data = True
                db.commit()
            if fetchall:
                data = sql.fetchall()
            if fetchone:
                data = sql.fetchone()
        return data

    def create_database(self):
        request = """CREATE TABLE IF NOT EXISTS url_ids(
                    url_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    use_status BOOLEAN
                    )"""
        self.execute(request)

    def create_url(self):
        request = "INSERT INTO url_ids(use_status) VALUES (?)"
        parameters = (False,)
        self.execute(request, parameters, commit=True)
        request = "SELECT MAX(url_id) FROM url_ids"
        return self.execute(request, fetchone=True)[0]

    def use_link(self, url_id):
        request = "UPDATE url_ids SET use_status = ? WHERE url_id = ?"
        parameters = (1, url_id)
        self.execute(request, parameters, commit=True)

    def check_url_id(self, url_id):
        request = "SELECT use_status FROM url_ids WHERE url_id = ?"
        parameters = (url_id,)
        return self.execute(request, parameters, fetchone=True)