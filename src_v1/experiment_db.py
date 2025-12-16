import sqlite3
import pandas as pd


def init_db(db="experiment.db"):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS exp_v1 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt_type TEXT,
                question TEXT,
                answer TEXT,
                token_usage INTEGER
            )
            """)
        con.commit()


def insert_entries(p_type, q, a, token_usage, db="experiment.db"):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        query = """
        INSERT INTO exp_v1 (prompt_type, question, answer, token_usage)
        VALUES(?, ?, ?, ?);
        """
        data = (p_type, q, a, token_usage)
        cur.execute(query, data)
        con.commit()


def print_entries(db="experiment.db"):
    with sqlite3.connect(db) as con:
        df = pd.read_sql_query("SELECT * FROM exp_v1;", con)
        print(df)


if __name__ == "__main__":
    init_db()
