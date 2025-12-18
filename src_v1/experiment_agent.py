import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

from db import insert_entries, print_entries, read_db_to_df
from experiment import get_prompt_template
from agent import Agent


if __name__ == "__main__":
    ########## Secrets ##########
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY_OPENAI")
    
    agent = Agent()
    """
    Der Agent bekommt jeden Tag unterschiedliche prompts mit denen er die Inhalte zusammenfassen soll.
    Die Zusammenfassungen werden von Nutzern im Nachinein bewertet

    Zero shot:
    Welche veganen Gerichte gibt es heute?    
    Gib mir Kleidungsempfehlungen für Hamburg.
    Few shot:
    Heute gibt es Linsensuppe. Oder heute gibt es veganen Auflauf. Jetzt gib mir heutige vegane Gerichte wieder.
    Es regnet also empfehle ich eine Regenjacke und feste Schuhe. Die Sonne scheint also empfehle ich luftige Kleidung. Jetz gibt mir Kleidungsempfehlungen für Hamburg.
    Chain of thought:
    Ich suche nach veganen Gerichten. Erst schaue ich, welche Gerichte verfügbar sind. Dann, ob sie tierische Produkte enthalten. Vegane Gerichte enthalten keine tierische Produkte, diese geben ich nun wieder, wenn sie heute serviert werden.
    Ich schaue nach wie das Wetter heute in Hamburg ist. Dann, ob es kalt oder warm ist. Dazu auch, ob es regnet oder windig ist. Wenn es kalt ist oder regnet, muss ich mich wärmer anziehen. Ich gebe nun eine Kleidungsempfehlung aus.
    Chain of draft:
    1. Essen für heute suchen 2. vegan != tierisch 3. vegan wiedergeben 
    1. Wetter Hamburg 2. kalt/warm + nass/trocken + windig? 3. Passende Kleidung empfehlen
    """
