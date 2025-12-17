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


def gen_data_presseportal(init=False):
    with sqlite3.connect("presseportal_prompts.db") as con:
        cur = con.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS presseportal_prompts (
            API_request TEXT,
            zero_shot TEXT,
            few_shot TEXT,
            chain_of_thought TEXT,
            chain_of_draft TEXT
        )
        """)
        if init:
            cur.execute("""
            INSERT INTO presseportal_prompts 
            (API_request, zero_shot, few_shot, chain_of_thought, chain_of_draft)
            VALUES (?, ?, ?, ?, ?)
            """, (
                "https://api.presseportal.de/api/v2/stories/police/image?api_key=yourapikey&limit=20&lang=de",
                "Retrieve the latest 20 police stories in german as images.",
                "Example:\n- https://api.presseportal.de/api/v2/stories/sports/image?api_key=yourapikey\n- https://api.presseportal.de/api/v2/stories/nature&lang=fr\nNow, fetch 20 police stories in in german form images.",
                "First, set the base-URL and then identify the storytype. Next, set the API key parameter. Then, specify the pagination start at 20. Also, set the language parameter. Finally, output the endpoint.",
                "1. base-URL 2. storytype 3. API key 4. 20 stories 5. language"
            ))

        con.commit()


if __name__ == "__main__":
    init_db()
    print_entries()
    print_entries(table="exp_agent_v1")
