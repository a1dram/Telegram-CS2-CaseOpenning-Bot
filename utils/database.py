import sqlite3
import time


class DB:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        try:
            with self.connection:
                return self.connection.execute("""INSERT INTO users ('user_id') VALUES (?)""", (user_id,))

        except sqlite3.IntegrityError:
            pass

    def add_user_name(self, user_id, name):
        with self.connection:
            return self.connection.execute("""UPDATE users SET user_name = ? WHERE user_id = ?""", (name, user_id))

    def add_user_money(self, user_id, user_money):
        with self.connection:
            return self.connection.execute("""UPDATE users SET user_money = ? WHERE user_id = ?""",
                                           (round(db.get_user_money(user_id) + float(user_money), 2), user_id))

    def add_inventory_sort(self, user_id, sort_type):
        with self.connection:
            return self.connection.execute("""UPDATE users SET inventory_sort = ? WHERE user_id = ?""",
                                           (sort_type, user_id))

    def add_language(self, user_id, language):
        with self.connection:
            return self.connection.execute("""UPDATE users SET language = ? WHERE user_id = ?""", (language, user_id))

    def add_inventory_capacity(self, user_id, inventory_capacity):
        with self.connection:
            return self.connection.execute("""UPDATE users SET inventory_capacity = ? WHERE user_id = ?""",
                                           (inventory_capacity, user_id))

    def add_user_items(self, user_id, user_items):
        with self.connection:
            return self.connection.execute("""UPDATE users SET user_items = ? WHERE user_id = ?""",
                                           (user_items, user_id))

    def add_quick_sell(self, user_id, quick_sell):
        with self.connection:
            return self.connection.execute("""UPDATE users SET quick_sell = ? WHERE user_id = ?""",
                                           (quick_sell, user_id))

    def get_user_name(self, user_id):
        with self.connection:
            return self.connection.execute(
                """SELECT user_name FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]

    def get_user_id(self, user_id):
        with self.connection:
            try:
                result = self.connection.execute("""SELECT user_id FROM users WHERE user_id = ?""",
                                                 (user_id,)).fetchmany(1)[0]

                return bool(len(result))

            except IndexError:
                return False

    def get_inventory_capacity(self, user_id):
        with self.connection:
            return self.connection.execute(
                """SELECT inventory_capacity FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]

    def get_user_items(self, user_id):
        with self.connection:
            return self.connection.execute(
                """SELECT user_items FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]

    def get_quick_sell(self, user_id):
        with self.connection:
            return self.connection.execute(
                """SELECT quick_sell FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]

    def get_inventory_sort(self, user_id):
        with self.connection:
            return self.connection.execute(
                """SELECT inventory_sort FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]

    def get_language(self, user_id):
        with self.connection:
            try:
                return self.connection.execute(
                    """SELECT language FROM users WHERE user_id = ?""", (user_id,)).fetchone()[0]
            except:
                pass

    def get_user_money(self, user_id):
        with self.connection:
            money = self.connection.execute("""SELECT user_money FROM users WHERE user_id = ?""",
                                            (user_id,)).fetchone()[0]

            return float(money)

    def get_all_user_ids(self):
        with self.connection:
            try:
                result = self.connection.execute("""SELECT user_id FROM users""").fetchall()

                return result

            except Exception as e:
                print('cs2_database.py error line 65:', e)
                pass


db = DB('database/cs2base.db')
