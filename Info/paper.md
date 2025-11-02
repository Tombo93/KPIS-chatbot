# paper

## Intro

## Methods

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
