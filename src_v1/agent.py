import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from api import get_rss_feed
from api import get_weather


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY_OPENAI")


class Agent:
    def __init__(self):
        self.sys_prompt = """Du bist ein hilfreicher Assistent, der ein RSS-Feed zu Essen zusammenfasst und mir Empfehlungen zur Klamottenwahl anhand der Wettervorhersage gibt.
                            Du hast Zugang zu zwei Tools:
                                - get_rss_feed: nutze dieses, um eine Anfrage an das RSS-Feed der Mensa zu stellen
                                - get_weather: nutze dieses, um die Wetterdaten von Norddeutschland zusammenzufassen und daraus Kleidungsempfehlungen abzuleiten
                                """
        model = ChatOpenAI(model="gpt-5-nano")
        self.agent = create_agent(
            model=model,
            tools=[get_rss_feed, get_weather], #hier können die zusätzlichen Tools eingefügt werden
            system_prompt=self.sys_prompt,
        )
    
    def invoke_stream(self, message_content, role="user"):
        for chunk in self.agent.stream({
            "messages": [{"role": role, "content": message_content}]
        }, stream_mode="values"):
            # Each chunk contains the full state at that point
            latest_message = chunk["messages"][-1]
            if latest_message.content:
                yield f"Agent: {latest_message.content}"
            elif latest_message.tool_calls:
                yield f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}"

    def invoke(self, message_content, role="user"):
        response = self.agent.invoke({"messages": [{"role": role, "content": message_content}]})
        return self.extract_response(response)
    
    def extract_response(self, agent_response):
        ai_message = agent_response["messages"][-1]
        return ai_message.content, ai_message.usage_metadata["total_tokens"]


if __name__ == "__main__":
    a = Agent()
    a.invoke_stream("Welche Gerichte gibt es heute? Sind vegane Gerichte dabei? Kannst du mir Kleidungsempfehlungen für Hamburg geben?")

