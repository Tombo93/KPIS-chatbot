import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.prompts import PromptTemplate


########## Configuration ##########
load_dotenv()
# API_KEY_PRESSEPORTAL = os.getenv("API_KEY_PRESSEPORTAL")
os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY_OPENAI")
# ------------------------------- #

########## Agent/Model Definition ##########
model = ChatOpenAI(model="gpt-5-nano")

SYSTEM_PROMPT = "Du bist ein neutraler Berichterstatter. Für Anfragen, die Code beinhalten liefere nur den Code. Du hältst dich kurz."
agent = create_agent(
    model=model,
    tools=[],
    system_prompt=SYSTEM_PROMPT,
)
# ---------------------------------- #

########## Experiment Definition ##########

# Load Data
example_data = {
    "datum": "03.01.2025",
    "tag1": "Polizei",
    "tag2": "Einsatz",
    "tag3": "öffentliche Ordnung",
    "bundesland": "Bayern",
    "titel": "Starkregen führte zu einzelnen Überschwemmungen von Kellern.",
    "text": "An diesem frostigen Januarmorgen führte die Augsburger Polizei eine Routinekontrolle durch  zumindest dachten alle, es sei Routine. Doch wahrend die Kontrolle fortschritt, bemerkte eine junge Polizistin eine unscheinbare Kiste auf dem Rücksitz eines alten Kombis. Darin fand sie ein kleines, mechanisches Uhrwerk, das ununterbrochen tickte, aber offenbar zu keiner Uhr gehörte."
}

# Load Prompts
example_prompts = {
    "base-prompt": "Erstelle eine Abfrage auf einem Pandas Dataframe, um die neuesten Nachrichten aus dem Bereich Politik abzurufen.",
    "conversational": "Ich möchte aktuelle politische Meldungen abrufen. Wie müsste eine Abfrage auf einem Pandas Dataframe aussehen, um genau das zu tun?",
    "chain-of-thought": "Ziel: Abrufen aktueller politischer Meldungen durch eine Abfrage auf einem Pandas Dataframe.\
        Kontext: Datenquelle ist ein Pandas Dataframe. Als Filter wird die Kategorie 'Politik' genutzt.\
        Nun Schritt für Schritt die Filterbedingungen entwickeln und den finalen Pandas-Ausdruck erzeugen."
}

# Prompt Template
prompt_template = PromptTemplate.from_template("Du bist ein neutraler Berichterstatter. Für Anfragen, die Code beinhalten liefere nur den Code. Du hältst dich kurz. Aufgabe: {query}")
prompts_list = [prompt_template.format(query=query) for _, query in example_prompts.items()]

# Generate Batch call to LLM with different configurations
responses = model.batch(prompts_list)

# Store responses
for response in responses:
    print(response)
# --------------------------------------- #