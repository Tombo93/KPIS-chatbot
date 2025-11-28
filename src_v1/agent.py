import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from api import get_rss_feed

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY_OPENAI")


model = ChatOpenAI(model="gpt-5-nano")

SYSTEM_PROMPT = """Du bist ein hilfreicher Assistent, der ein RSS-Feed zu Essen zusammenfasst.
    
    Du hast Zugang zu einem Tool:
    
    - get_rss_feed: nutze dieses, um eine Anfrage an das RSS-Feed der Mensa zu stellen
    """

agent = create_agent(
    model=model,
    tools=[get_rss_feed],
    system_prompt=SYSTEM_PROMPT,
)

for chunk in agent.stream({
    "messages": [{"role": "user", "content": "Welche Gerichte gibt es heute? Sind vegane Gerichte dabei?"}]
}, stream_mode="values"):
    # Each chunk contains the full state at that point
    latest_message = chunk["messages"][-1]
    if latest_message.content:
        print(f"Agent: {latest_message.content}")
    elif latest_message.tool_calls:
        print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")
