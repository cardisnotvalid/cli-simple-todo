from typing import Optional, List

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from dataclasses import dataclass, asdict

from logger import log

SQL_INIT_TABLE = (
    "CREATE TABLE IF NOT EXISTS Todo ("
    "id INTEGER PRIMARY KEY,"
    "checked BOOLEAN,"
    "name CHARVAR(256) NOT NULL,"
    "created_at DATE"
    ");"
)


@dataclass
class Todo:
    id: int
    checked: bool
    name: str
    created_at: str

    def dict(self) -> dict:
        return {k: str(v) for k, v in asdict(self).items()}


class Connector:
    DB_PATH = "todo.sqlite3"

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.DB_PATH)
        try:
            yield conn
        except sqlite3.Error as err:
            conn.rollback()
            raise err
        else:
            conn.commit()
        finally:
            conn.close()


class SQLBuilder:
    @staticmethod
    def select(what, where=None):
        sql = f"SELECT {what} FROM Todo"
        if where: sql += f" WHERE {where}=?"
        return sql

    @staticmethod
    def select_all(where=None):
        sql = f"SELECT * FROM Todo"
        if where: sql += f" WHERE {where}=?"
        return sql

    @staticmethod
    def insert(*what):
        val = ",".join("?" * len(what))
        return f"INSERT INTO Todo({','.join(what)}) VALUES({val})"

    @staticmethod
    def drop(where):
        return f"DELETE FROM Todo WHERE {where}=?"

    @staticmethod
    def update(what, where):
        return f"UPDATE Todo SET {what}=? WHERE {where}=?"


class DBManager(Connector):
    def __init__(self) -> None:
        super().__init__()
        self._init_table()

    def _init_table(self) -> None:
        self.conn.execute(SQL_INIT_TABLE)

    def get(self, id) -> Todo:
        sql = SQLBuilder.select_all("id")
        curr = self.conn.cursor()
        if data := curr.execute(sql, (id,)).fetchone():
            return Todo(*data)
        return

    def get_all(self) -> List[Todo]:
        sql = SQLBuilder.select_all()
        curr = self.conn.cursor()
        data = curr.execute(sql).fetchall()
        return [Todo(*todo) for todo in data[::-1]]

    def add(self, name: str, *, checked=False) -> bool:
        sql = SQLBuilder.select_all("name")
        curr = self.conn.cursor()
        if curr.execute(sql, (name,)).fetchone():
            log("WARNING", f"Todo(name={name}) already exists")
            return False

        sql = SQLBuilder.insert("checked", "name", "created_at")
        curr_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conn.execute(sql, (checked, name, curr_date))
        log("SUCCESS", f"Todo(name={name}) added")
        return True

    def delete(self, id) -> bool:
        if not self.get(id):
            log("WARNING", f"Todo(id={id}) does not exists")
            return False

        sql = SQLBuilder.drop("id")
        self.conn.execute(sql, (id,))
        log("SUCCESS", f"Todo(id={id}) deleted")
        return True

    def update(self, id, checked) -> bool:
        if not self.get(id):
            log("WARNING", f"Todo(id={id}) does not exists")
            return False

        sql = SQLBuilder.update("checked", "id")
        self.conn.execute(sql, (checked, id))
        log("SUCCESS", f"Todo(id={id}) updated")
        return True


def db_handler(func):
    def wrapper(*args, **kwargs):
        with DBManager() as db:
            return func(db, *args, **kwargs)
    return wrapper


if __name__ == "__main__":
    with DBManager() as db:
        # db.add("Физкультура")
        # db.add("Помыть посуду, после обеда")
        # db.add("Пройтись по магазинам, купить продукты")
        pass
