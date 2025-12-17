import sqlite3
import pandas as pd


def init_db():
    with sqlite3.connect("experiment.db") as con:
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
        cur.execute("""
            CREATE TABLE IF NOT EXISTS exp_agent_v1 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                answer TEXT,
                token_usage INTEGER
            )
            """)
        con.commit()


def alter_table():
    with sqlite3.connect("experiment.db") as con:
        cur = con.cursor()
        cur.execute("ALTER TABLE exp_v1 DROP COLUMN CLOUMN")
        cur.execute("ALTER TABLE exp_v1 ADD COLUMN API_request TEXT")
        con.commit()


def insert_entries(q, a, token_usage, api_request, p_type="zero-shot", table="exp_v1"):
    with sqlite3.connect("experiment.db") as con:
        cur = con.cursor()
        match table:
            case "exp_v1":
                query = """
                INSERT INTO exp_v1 (prompt_type, question, answer, token_usage, API_request)
                VALUES(?, ?, ?, ?, ?);
                """
                data = (p_type, q, a, token_usage, api_request)
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


def read_db_to_df(db="presseportal_prompts.db", table="presseportal_prompts"):
    with sqlite3.connect(db) as con:
        q = f"SELECT * FROM {table};"
        df = pd.read_sql_query(q, con)
    return df


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
            entries = [(
                "https://api.presseportal.de/api/v2/stories/politics/image?api_key=yourapikey&limit=20&lang=de",
                "Retrieve the latest 20 politics stories in German as images.",
                "Example:\n- https://api.presseportal.de/api/v2/stories/sports/image?api_key=yourapikey\n- https://api.presseportal.de/api/v2/stories/nature&lang=fr\nNow, fetch 20 politics stories in German as images.",
                "First, set the base-URL and then identify the storytype. Next, set the API key parameter. Then, specify the limit of 20. Also, set the language parameter. Finally, output the endpoint.",
                "1. base-URL 2. storytype 3. API key 4. 20 stories 5. language"
            ),
            (
                "https://api.presseportal.de/api/v2/stories/sports?api_key=yourapikey&start=10&limit=15&lang=en",
                "Retrieve 15 sports stories in English starting from offset 10.",
                "Example:\n- https://api.presseportal.de/api/v2/stories/health/image?api_key=yourapikey\n- https://api.presseportal.de/api/v2/stories/economy&lang=de\nNow, fetch 15 sports stories in English starting at offset 10.",
                "First, set the base-URL and then identify the storytype. Next, set the API key parameter. Then, specify the pagination start at 10. Also, set the language parameter. Finally, output the endpoint.",
                "1. base-URL 2. storytype 3. API key 4. 15 stories 5. start offset 10 6. language"
            ),
            (
                "https://api.presseportal.de/api/v2/stories/nature?api_key=yourapikey&limit=30&lang=fr",
                "Retrieve the latest 30 nature stories in French.",
                "Example:\n- https://api.presseportal.de/api/v2/stories/police/image?api_key=yourapikey\n- https://api.presseportal.de/api/v2/stories/science&lang=es\nNow, fetch 30 nature stories in French.",
                "First, set the base-URL and then identify the storytype. Next, set the API key parameter. Then, specify the limit of 30. Also, set the language parameter. Finally, output the endpoint.",
                "1. base-URL 2. storytype 3. API key 4. 30 stories 5. language"
            ),
            (
                "https://api.presseportal.de/api/v2/stories/health/image?api_key=yourapikey&limit=25&lang=de&encoded=1",
                "Retrieve the latest 25 health stories in German as images with HTML-encoded body.",
                "Example:\n- https://api.presseportal.de/api/v2/stories/science/image?api_key=yourapikey\n- https://api.presseportal.de/api/v2/stories/travel&lang=es\nNow, fetch 25 health stories in German as images with encoded body.",
                "First, set the base-URL and then identify the storytype. Next, set the API key parameter. Then, specify the limit of 25. Also, set the language parameter and encoded=1. Finally, output the endpoint.",
                "1. base-URL 2. storytype 3. API key 4. 25 stories 5. language 6. encoded body"
            ),
            (
                "https://api.presseportal.de/api/v2/stories/economy?api_key=yourapikey&limit=50&lang=en",
                "Retrieve the latest 50 economy stories in English.",
                "Example:\n- https://api.presseportal.de/api/v2/stories/police/image?api_key=yourapikey\n- https://api.presseportal.de/api/v2/stories/nature&lang=fr\nNow, fetch 50 economy stories in English.",
                "First, set the base-URL and then identify the storytype. Next, set the API key parameter. Then, specify the limit of 50. Also, set the language parameter. Finally, output the endpoint.",
                "1. base-URL 2. storytype 3. API key 4. 50 stories 5. language"
            ),
            (
                "https://api.presseportal.de/api/v2/stories/science/image?api_key=yourapikey&start=5&limit=5&lang=es",
                "Retrieve 5 science stories in Spanish as images starting from offset 5.",
                "Example:\n- https://api.presseportal.de/api/v2/stories/health/image?api_key=yourapikey\n- https://api.presseportal.de/api/v2/stories/politics&lang=de\nNow, fetch 5 science stories in Spanish as images starting at offset 5.",
                "First, set the base-URL and then identify the storytype. Next, set the API key parameter. Then, specify the pagination start at 5. Also, set the language parameter. Finally, output the endpoint.",
                "1. base-URL 2. storytype 3. API key 4. 5 stories 5. start offset 5 6. language"
            ),
            (
                "https://api.presseportal.de/api/v2/stories/travel?api_key=yourapikey&limit=40&lang=it",
                "Retrieve the latest 40 travel stories in Italian.",
                "Example:\n- https://api.presseportal.de/api/v2/stories/nature/image?api_key=yourapikey\n- https://api.presseportal.de/api/v2/stories/health&lang=fr\nNow, fetch 40 travel stories in Italian.",
                "First, set the base-URL and then identify the storytype. Next, set the API key parameter. Then, specify the limit of 40. Also, set the language parameter. Finally, output the endpoint.",
                "1. base-URL 2. storytype 3. API key 4. 40 stories 5. language"
            ),
            (
                "https://api.presseportal.de/api/v2/stories/technology/image?api_key=yourapikey&limit=12&lang=en&encoded=1",
                "Retrieve the latest 12 technology stories in English as images with HTML-encoded body.",
                "Example:\n- https://api.presseportal.de/api/v2/stories/economy/image?api_key=yourapikey\n- https://api.presseportal.de/api/v2/stories/science&lang=de\nNow, fetch 12 technology stories in English as images with encoded body.",
                "First, set the base-URL and then identify the storytype. Next, set the API key parameter. Then, specify the limit of 12. Also, set the language parameter and encoded=1. Finally, output the endpoint.",
                "1. base-URL 2. storytype 3. API key 4. 12 stories 5. language 6. encoded body"
            ),
            (
                "https://api.presseportal.de/api/v2/stories/technology/image?api_key=yourapikey&limit=12&lang=en&encoded=1",
                "Retrieve the latest 12 technology stories in English as images with HTML-encoded body.",
                "Example:\n- https://api.presseportal.de/api/v2/stories/economy/image?api_key=yourapikey\n- https://api.presseportal.de/api/v2/stories/science&lang=de\nNow, fetch 12 technology stories in English as images with encoded body.",
                "First, set the base-URL and then identify the storytype. Next, set the API key parameter. Then, specify the limit of 12. Also, set the language parameter and encoded=1. Finally, output the endpoint.",
                "1. base-URL 2. storytype 3. API key 4. 12 stories 5. language 6. encoded body"
            ),
            (
                "https://api.presseportal.de/api/v2/stories/education?api_key=yourapikey&start=20&limit=10&lang=de",
                "Retrieve 10 education stories in German starting from offset 20.",
                "Example:\n- https://api.presseportal.de/api/v2/stories/politics/image?api_key=yourapikey\n- https://api.presseportal.de/api/v2/stories/travel&lang=fr\nNow, fetch 10 education stories in German starting at offset 20.",
                "First, set the base-URL and then identify the storytype. Next, set the API key parameter. Then, specify the pagination start at 20. Also, set the language parameter. Finally, output the endpoint.",
                "1. base-URL 2. storytype 3. API key 4. 10 stories 5. start offset 20 6. language"
            ),
            (
                "https://api.presseportal.de/api/v2/stories/entertainment/image?api_key=yourapikey&limit=18&lang=fr",
                "Retrieve the latest 18 entertainment stories in French as images.",
                "Example:\n- https://api.presseportal.de/api/v2/stories/science/image?api_key=yourapikey\n- https://api.presseportal.de/api/v2/stories/health&lang=es\nNow, fetch 18 entertainment stories in French as images.",
                "First, set the base-URL and then identify the storytype. Next, set the API key parameter. Then, specify the limit of 18. Also, set the language parameter. Finally, output the endpoint.",
                "1. base-URL 2. storytype 3. API key 4. 18 stories 5. language"
            )]
            cur.executemany("""
            INSERT INTO presseportal_prompts 
            (API_request, zero_shot, few_shot, chain_of_thought, chain_of_draft)
            VALUES (?, ?, ?, ?, ?);
            """, entries)

        con.commit()


if __name__ == "__main__":
    print_entries()
    print_entries(table="exp_agent_v1")