import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from experiment_db import insert_entries, print_entries


########## Configuration ##########
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY_OPENAI")
# ------------------------------- #

########## Model Definition ##########
model = ChatOpenAI(model="gpt-5-nano")
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
    "base-prompt": "Erstelle eine Abfrage auf der Pressportal API, um die neuesten Nachrichten aus dem Bereich Politik abzurufen.",
    "conversational": "Ich möchte aktuelle politische Meldungen abrufen. Wie müsste eine Abfrage auf der Pressportal API aussehen, um genau das zu tun?",
    "chain-of-thought": "Ziel: Abrufen aktueller politischer Meldungen durch eine Abfrage auf der Pressportal API.\
        Kontext: Datenquelle ist die Pressportal API. Als Filter wird die Kategorie 'Politik' genutzt.\
        Nun Schritt für Schritt die Filterbedingungen entwickeln und den finalen Pandas-Ausdruck erzeugen."
}
# Prompt Templates
# for zero & few shot prompts
standard = PromptTemplate.from_template("Answer the question directly. Do not return any preamble, explanation, or reasoning. Aufgabe: {query}")
chain_of_though = PromptTemplate.from_template("Think step by step to answer the following question. Return the answer at the end of the response after a separator ####. Aufgabe: {query}")
chain_of_draft = PromptTemplate.from_template("Think step by step, but only keep a minimum draft for each thinking step, with 5 words at most. Return the answer at the end of the response after a separator ####. Aufgabe: {query}")

zero_shot = [standard.format(query=example_prompts["base-prompt"])]

# Generate Batch call to LLM with different configurations
responses = model.batch(zero_shot)

# Store responses
for q, a in zip(zero_shot, responses):
    insert_entries("zero-shot", q, a.content, a.response_metadata['token_usage']['total_tokens'])
# --------------------------------------- #
print_entries()
