# Prentenmapper backend

Deze repository bevat een simpel servertje dat gemaakt en gebruikt is in de [Hack-a-LOD 2018][hal2018] door [Team UB Leiden][ubl-hackalod].
De server ontvangt een simpel verzoek en stuurt SPARQL-query's naar het [SPARQL-endpoint van de KB][kb-sparql] en het [SPARQL-endpoint van Wikidata][wd-sparql]. Het resultaat van de SPARQL-query wordt doorgegeven.

Hoewel het idee van de Prentenmapper ook gebruikersaccounts en scores omvat, is er nog geen enkele stap gezet om dit te implementeren.

[hal2018]: http://hackalod.com/
[ubl-hackalod]: https://www.bibliotheek.universiteitleiden.nl/nieuws/2018/02/team-ubleiden-wint-publieksprijs-hackathon
[kb-sparql]: http://lod.kb.nl/sparql
[wd-sparql]: https://query.wikidata.org/sparql

## Installatie

Tijdens de Hack-a-LOD is een Docker container gebruikt, maar je kunt de server ook direct met Python 3 gebruiken.

### Docker

Met [Docker][docker] kun je de server op allerlei platforms draaien en heb je naast Docker zelf geen afhankelijkheden. Zie de [Docker-handleiding][docker-man] voor een inleiding.

[docker]: https://www.docker.com
[docker-man]: https://docs.docker.com/

Op een Linux-machine met een recente versie van Docker kun je een container starten op basis van een door ons gebouwd image:

<kbd>sudo docker pull leidenuniversitylibraries/prentenmapper-api</kbd>

Je kunt ook zelf een image maken met de bijgevoegde Dockerfile:

<kbd>sudo docker build -t prentenmapper-api .</kbd>

### Python 3

De Prentenmapper backend is ontwikkeld met Python 3.6 en maakt o.a. gebruik van [`aiohttp`][aiohttp] dat gebruik maakt van `asyncio`. Eerdere versies van Python 3 zijn daardoor mogelijk niet geschikt.

[aiohttp]: https://aiohttp.readthedocs.io/en/stable/

Het is aan te raden om een `virtualenv` te gebruiken voor de Prentenmapper backend. Met de gemaakte `virtualenv` geactiveerd installeer je de benodigdheden met:

<kbd>git clone https://github.com/LeidenUniversityLibrary/prentenmapper-api.git</kbd>  
<kbd>cd prentenmapper-api</kbd>  
<kbd>pip install -r requirements.txt</kbd>

## Gebruik

Deze server is gemaakt om te gebruiken in combinatie met de [Prentenmapper app][app]. Omdat het eigenlijk een schil is om de SPARQL-endpoints van de KB en Wikidata, werkt de Prentenmapper alleen als deze endpoints beschikbaar zijn.

[app]: https://github.com/LeidenUniversityLibrary/PrentenMapperApp

Met onderstaande instructies start je de serverapplicatie op poort 5000. Als er een firewall actief is, is de kans groot dat de applicatie dan niet via het Internet bereikbaar is. Met een *reverse proxy* kun je de serverapplicatie bereikbaar maken op bijvoorbeeld poort 80 (HTTP) of 443 (HTTPS, mits de servercertificaten goed zijn ingesteld).

### Docker

Als je het image dat Team UB Leiden heeft gepubliceerd hebt gedownload, kun je dat starten met:

<kbd>sudo docker run -p 5000:5000 -d leidenuniversitylibraries/prentenmapper-api</kbd>

Als je zelf een image hebt gemaakt, kun je dat op vergelijkbare wijze starten met:

<kbd>sudo docker run -p 5000:5000 -d prentenmapper-api</kbd>

De server is in beide gevallen beschikbaar op `[host]:5000/`.

### Python 3

Met de `virtualenv` geactiveerd, start je de server vanuit de directory waarin de code staat met:

<kbd>python prentenmapper.py</kbd>

De server draait dan op `[host]:5000` en logs worden naar de standard out geschreven.

## Licentie

De Prentenmapper backend is geschreven door Ben Companjen. © 2018, [Universitaire Bibliotheken Leiden][ubl].

Dit is vrije software. Gebruik etc. is toegestaan onder de voorwaarden van de [General Public License, versie 3][gplv3].

[ubl]: https://www.bibliotheek.universiteitleiden.nl/
[gplv3]: http://www.gnu.org/licenses/gpl-3.0.txt
