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

# Load Prompts
example_prompts = {
    "base-prompt": "Erstelle eine Abfrage auf der Pressportal API, um die neuesten Nachrichten aus dem Bereich Politik abzurufen.",
    "conversational": "Ich möchte aktuelle politische Meldungen abrufen. Wie müsste eine Abfrage auf der Pressportal API aussehen, um genau das zu tun?",
    "chain-of-thought": "Ziel: Abrufen aktueller politischer Meldungen durch eine Abfrage auf der Pressportal API.\
        Kontext: Datenquelle ist die Pressportal API. Als Filter wird die Kategorie 'Politik' genutzt.\
        Nun Schritt für Schritt die Filterbedingungen entwickeln und den finalen Pandas-Ausdruck erzeugen."
}
# Prompt Templates
# for zero & few shot prompts requesting the Presseportal API
zero_shot = PromptTemplate.from_template(
    "{sys_prompt} Answer the question directly. Do not return any preamble, explanation, or reasoning. Question: {query}"
)
few_shot = PromptTemplate.from_template(
    "{sys_prompt} Answer the question directly. Do not return any preamble, explanation, or reasoning. Question: {query}"
)
chain_of_though = PromptTemplate.from_template(
    "{sys_prompt} Think step by step to answer the following question. Return the answer at the end of the response after a separator ####. Question: {query}"
)
chain_of_draft = PromptTemplate.from_template(
    "{sys_prompt} Think step by step, but only keep a minimum draft for each thinking step, with 5 words at most. Return the answer at the end of the response after a separator ####. Question: {query}"
)

zero_shot = [zero_shot.format(query=example_prompts["base-prompt"], sys_prompt="You are generating an API URL for the Presseportal API.")]

# Generate Batch call to LLM with different configurations
responses = model.batch(zero_shot)

# Store responses
for q, a in zip(zero_shot, responses):
    insert_entries(q, a.content, a.response_metadata['token_usage']['total_tokens'], p_type="zero-shot")
# --------------------------------------- #
print_entries()
