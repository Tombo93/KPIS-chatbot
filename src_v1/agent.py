import os
import pandas as pd
from dotenv import load_dotenv
from langchain.agents import create_agent

########## Helpers ##########
def filter_df_by_col(df, col, search_string):
    df = df[df[col].str.contains(search_string)]
    return df
# ------------------------- #


########## Configuration ##########
load_dotenv()
API_KEY_PRESSEPORTAL = os.getenv("API_KEY_PRESSEPORTAL")
API_KEY_LLM = os.getenv("API_KEY_OPENAI")
# ------------------------------- #


########## Data ##########
data = pd.read_csv("artikel-fiktiv.csv")
filtered_data = filter_df_by_col(data, "tags", "Polizei")
print(filtered_data)
# ------------------------------- #


# prompts = pd.read_csv("prompts.csv")
# agent = create_agent(
#     model="gpt-4o",
#     tools=[],
#     system_prompt="You are a helpful assistant",
# )

# # Run the agent
# agent.invoke({"messages": [{"role": "user", "content": "what is the weather in sf"}]})
