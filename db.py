import sqlite3


class SQLRequests:
    def __init__(self, way_database: str):
        self.connection = sqlite3.connect(way_database)
        self.cursor = self.connection.cursor()

    def user_exists(self, user: int) -> bool:
        request = """SELECT * FROM `yawns_user` WHERE `user` = ?"""
        data = (user,)
        result = self.cursor.execute(request, data).fetchone()
        return True if result else False

    def add_user(self, user: int):
        request = """INSERT INTO `yawns_user` (`user`) VALUES(?)"""
        data = (user,)
        self.cursor.execute(request, data)
        self.connection.commit()

    def new_date(self, user: int, date: str):
        request = """SELECT `dates` FROM `yawns_user` WHERE `user` = ?"""
        data = (user,)
        current_dates = self.cursor.execute(request, data).fetchone()[0]
        text = ('' if not current_dates else current_dates) + date + ','

        request = """UPDATE `yawns_user` SET dates = ? WHERE user = ?"""
        data = (text, user)
        self.cursor.execute(request, data)
        self.connection.commit()

    def get_dates(self, user: int) -> str or bool:
        request = """SELECT `dates` FROM `yawns_user` WHERE `user` = ?"""
        data = (user,)
        result = self.cursor.execute(request, data).fetchone()[0]
        return result.split(',')[:-1] if result else []
