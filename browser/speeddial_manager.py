from database.db_manager import DatabaseManager

class SpeedDialManager:
    @staticmethod
    def get_all():
        cur = DatabaseManager._connection.execute("SELECT title, url FROM speed_dial ORDER BY id")
        return cur.fetchall()

    @staticmethod
    def add(title, url):
        DatabaseManager._connection.execute("INSERT OR IGNORE INTO speed_dial (title, url) VALUES (?, ?)", (title, url))
        DatabaseManager._connection.commit()

    @staticmethod
    def remove(url):
        DatabaseManager._connection.execute("DELETE FROM speed_dial WHERE url=?", (url,))
        DatabaseManager._connection.commit()