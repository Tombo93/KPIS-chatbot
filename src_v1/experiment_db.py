import sqlite3
import pandas as pd


def init_db():
    with sqlite3.connect("experiment.db") as con:
        cur = con.cursor()
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS exp_v1 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt_type TEXT,
                question TEXT,
                answer TEXT,
                token_usage INTEGER
            )
            """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS exp_agent_v1 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                answer TEXT,
                token_usage INTEGER
            )
            """)
        con.commit()


def insert_entries(q, a, token_usage, p_type="zero-shot", table="exp_v1"):
    with sqlite3.connect("experiment.db") as con:
        cur = con.cursor()
        match table:
            case "exp_v1":
                query = """
                INSERT INTO exp_v1 (prompt_type, question, answer, token_usage)
                VALUES(?, ?, ?, ?);
                """
                data = (p_type, q, a, token_usage)
            case "exp_agent_v1":
                query = """
                INSERT INTO exp_agent_v1 (question, answer, token_usage)
                VALUES(?, ?, ?);
                """
                data = (q, a, token_usage)
        cur.execute(query, data)
        con.commit()


def print_entries(table="exp_v1"):
    with sqlite3.connect("experiment.db") as con:
        q = f"SELECT * FROM {table};"
        df = pd.read_sql_query(q, con)
        print(f"Table {table}")
        print("####")
        print(df)


if __name__ == "__main__":
    init_db()
    print_entries()
    print_entries(table="exp_agent_v1")
