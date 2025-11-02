# paper

## Intro


## III. PROMPT CLASSES AND TASK DEFINITION
Based on the existing literature, this section will describe
the prompt classes that we chose for the experimental design
as well es the task definition for the Chatbot.

---


## IV. EVALUATION METRICS AND METHOD
Based on the existing literature, this section will describe
the the evaluation metrics and methods

---


## V. Experimental Design
This section will describe the technical setup of the chatbot system and the experimental workflow.
The chatbot will integrate retrieval access to the Presseportal with an LLM interface.
Each prompt variant will be systematically tested across a consistent set of articles.
The process will include data selection, prompt injection, output collection, and evaluation.

---

This section will describe the technical setup of the chatbot system and the experimental workflow.
The chatbot will integrate retrieval access to the Presseportal with an LLM interface.
Each prompt variant will be systematically tested across a consistent set of articles.
The process will include data selection, prompt crafting(injection), output collection, and evaluation.

## Data

### Mediastack
- Alternative für die Pressestelle API (https://mediastack.com/documentation)
- Umfangreiche keywords-Suche
- ABER nur 100 Calls / Monat bei 0 €

### newsapi
- 2000 Suchen für den free plan
- Python interface für requests
- (https://newsapi.ai/)

### Pressestelle
- Hierfür müssen wir einen API-Key beantragen, was etwas Zeit in anspruch nehmen kann.
- Kann man die API für unsere Zwecke nutzen?
> Es lassen sich verschiedenste API-Calls erstellen.
> Z.B. kann man nach Story-Topic filern: api/v2/stories/topic/sport
> Oder man kann nach office-Type filtern: api/v2/stories/police/officetype/zoll

Da die Parameter der API sich eher auf Details zu einer Story beziehen und es davon nicht allzu viele gibt, könnte sich die Auswertung der erstellten API-Calls als nicht so ergiebig herausstellen.
URL-Parameter sind z.B.: start, limit, lang, encoded => api/v2/.../stories?start=1&limit=20

#### Als Test die Anfrage an Copilot:

- Spannend zu sehen ist hier jedoch, dass die generierten API-Calls nicht der Spezifikation auf der Website entsprechen
Hier aus der Dokumentation
> GET https://api.presseportal.de/api/v2/stories/topic/sport?api_key=yourapikey&start=20

Und hier aus Copilot:

Generiere mir einen API-Call zum deutschen presseportal für Stories mit dem Thema Sport
> GET https://api.presseportal.de/api/v1/news?query=Sport&limit=10&sort=date_desc

generiere den API-call nun für artikel auf englisch
> GET https://api.presseportal.de/api/v1/news?query=Sport&language=en&limit=10&sort=date_desc
