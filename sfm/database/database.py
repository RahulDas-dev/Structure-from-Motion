import sqlite3

from sfm.database.db_scripts import create_table_statement


class Dtatabase:
    def __init__(self, db_path: str):
        self._connection = None
        self.connected = False
        self.db_path = db_path

    def connection(self):
        """Create SQL connection"""
        if self.connected:
            return self._connection
        self._connection = sqlite3.connect(self.db_path)
        self.__create_tables()
        self.connected = True
        return self._connection

    def __create_tables(self):
        self.executescript(create_table_statement)

    def close(self):
        """Close SQL connection"""
        if self.connected:
            self.connection.close()
        self.connected = False

    def commit(self):
        """Commit SQL changes"""
        self.connection.commit()

    def execute(self, sql, *args):
        """Execute SQL"""
        return self.connection.execute(sql, args)

    def executescript(self, script: str):
        """Execute SQL script"""
        self.connection.cursor().executescript(script)
        self.commit()
