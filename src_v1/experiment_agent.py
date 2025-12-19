import os
from dotenv import load_dotenv

from agent import Agent
from db import insert_entries, print_entries


if __name__ == "__main__":
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY_OPENAI")
    
    prompt_types = {
        "zero_shot" : "Welche veganen Gerichte gibt es heute?; Gib mir Kleidungsempfehlungen für Hamburg.",
        "few_shot": "Heute gibt es Linsensuppe. Oder heute gibt es veganen Auflauf. Jetzt gib mir heutige vegane Gerichte wieder.; Es regnet also empfehle ich eine Regenjacke und feste Schuhe. Die Sonne scheint also empfehle ich luftige Kleidung. Jetz gibt mir Kleidungsempfehlungen für Hamburg.",
        "chain_of_thought": "Ich suche nach veganen Gerichten. Erst schaue ich, welche Gerichte verfügbar sind. Dann, ob sie tierische Produkte enthalten. Vegane Gerichte enthalten keine tierische Produkte, diese geben ich nun wieder, wenn sie heute serviert werden.;Ich schaue nach wie das Wetter heute in Hamburg ist. Dann, ob es kalt oder warm ist. Dazu auch, ob es regnet oder windig ist. Wenn es kalt ist oder regnet, muss ich mich wärmer anziehen. Ich gebe nun eine Kleidungsempfehlung aus.",
        "chain_of_draft": "1. Essen für heute suchen 2. vegan != tierisch 3. vegan wiedergeben; 1. Wetter Hamburg 2. kalt/warm + nass/trocken + windig? 3. Passende Kleidung empfehlen"
    }
  
    agent = Agent()
    for p_type, prompt in prompt_types.items():
        answer, token_usage = agent.invoke(prompt)
        insert_entries(prompt, answer, token_usage, None, p_type=p_type, table="exp_agent_v1")
    print_entries(table="exp_agent_v1")
