import os
import pandas as pd
from dotenv import load_dotenv
from langchain.agents import create_agent


load_dotenv()
API_KEY_PRESSEPORTAL = os.getenv("API_KEY_PRESSEPORTAL")
API_KEY_LLM = os.getenv("API_KEY_OPENAI")

prompts = pd.read_csv("prompts.csv")

agent = create_agent(
    model="gpt-4o",
    tools=[],
    system_prompt="You are a helpful assistant",
)

# Run the agent
agent.invoke({"messages": [{"role": "user", "content": "what is the weather in sf"}]})
