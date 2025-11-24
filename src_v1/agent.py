import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

########## Helpers ##########
def filter_df_by_col(df, col, search_string):
    df = df[df[col].str.contains(search_string)]
    return df
# ------------------------- #


########## Configuration ##########
load_dotenv()
# API_KEY_PRESSEPORTAL = os.getenv("API_KEY_PRESSEPORTAL")
os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY_OPENAI")
# ------------------------------- #


########## Data ##########
data = pd.read_csv("artikel-fiktiv.csv")
filtered_data = filter_df_by_col(data, "tags", "Polizei")
# print(filtered_data)
prompts = pd.read_csv("prompts.csv")
# ------------------------------- #


########## Agent Definition ##########
model = ChatOpenAI(model="gpt-5-nano")

SYSTEM_PROMPT = "Du bist ein neutraler Berichterstatter"

agent = create_agent(
    model=model,
    tools=[],
    system_prompt=SYSTEM_PROMPT,
)
# ---------------------------------- #


########## Experiment Definition ##########
response = agent.invoke({"messages": [{"role": "user", "content": "Generiere einen API-Call ans deutsche Presseportal mit Stories zu Berlin"}]})

print(response)
# --------------------------------------- #