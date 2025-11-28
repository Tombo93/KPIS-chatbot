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
    
    - get_rss_feed: nutze dieses, um eine Anfrage an das RSS-Feed der Mensa Stellingen zu stellen
    
    Wenn du gefragt wirst was es zu essen gibt, gibts du eine Zusammenfassung des Feeds wieder."""

agent = create_agent(
    model=model,
    tools=[get_rss_feed],
    system_prompt=SYSTEM_PROMPT,
)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "Was gibt es heute in der Mensa Stellingenzu essen?"}]}
)
print(response)
