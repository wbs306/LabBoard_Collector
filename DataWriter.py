import sqlite3

class DataWriter:
    def __init__(self, db_path, data_dicts=None):
        self._db = sqlite3.connect(db_path)
        self._cursor = self._db.cursor()

        if (data_dicts):
            for name, t_dict in data_dicts.items():
                create_str = f"create table {name} (date DATE,"
                pair = list(t_dict.items())
                for i in range(len(pair) - 1):
                    create_str += f"{pair[i][0]} {pair[i][1]},"
                create_str += f"{pair[-1][0]} {pair[-1][1]})"
                self._cursor.execute(create_str)

    def write(self, table, data):
        insert_str = f"insert into {table} values("
        for i in range(len(data) - 1):
            insert_str += f"{data[i]},"
        insert_str += f"{data[-1]})"
        self._cursor.execute(insert_str)
        self._db.commit()