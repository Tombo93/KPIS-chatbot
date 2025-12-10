import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from dataclasses import dataclass
from langchain.tools import tool#, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.structured_output import ToolStrategy

from api import get_rss_feed
from api import get_weather


checkpointer = InMemorySaver()

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY_OPENAI")


model = ChatOpenAI(model="gpt-5-nano")

SYSTEM_PROMPT = """Du bist ein hilfreicher Assistent, der ein RSS-Feed zu Essen zusammenfasst und mir Empfehlungen zur Klamottenwahl anhand der Wettervorhersage gibt.
    
    Du hast Zugang zu zwei Tools:
    
    - get_rss_feed: nutze dieses, um eine Anfrage an das RSS-Feed der Mensa zu stellen
    - get_weather: nutze dieses, um die Wetterdaten von Norddeutschland zusammenzufassen und daraus Kleidungsempfehlungen abzuleiten
    """


@dataclass 
class Context:
    """Custom runtime context schema."""
    user_id: str

class ResponseFormat:
    """Response schema for the agent."""
    # A funny response (always required)
    funny_response: str
    # Any interesting information about the weather if available
    weather_conditions: str | None = None


agent = create_agent(
    model=model,
    tools=[get_rss_feed, get_weather], #hier können die zusätzlichen Tools eingefügt werden
    #context_format=Context,
    response_format=ToolStrategy(ResponseFormat),
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer
)

# `thread_id` is a unique identifier for a given conversation.
config = {"configurable": {"thread_id": "1"}}

for chunk in agent.stream({
    "messages": [{"role": "user", "content": "Welche Gerichte gibt es heute? Sind vegane Gerichte dabei? Kannst du mir Kleidungsempfehlungen für Hamburg geben?"}]
}, stream_mode="values"):
    # Each chunk contains the full state at that point
    latest_message = chunk["messages"][-1]
    if latest_message.content:
        print(f"Agent: {latest_message.content}")
    elif latest_message.tool_calls:
        print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")
