# Wrapper voor SPARQL-query's

from aiohttp import web
import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON

SPARQL_URI = "http://lod.kb.nl/sparql"
SPARQL_QUERY = """
select ?photo ?title ?description ?place ?extent ?image
where {
  ?photo a dctype:StillImage ;
    dcterms:spatial ?place .
  FILTER(REGEX(?place, "Amsterdam"))

  ?photo dcterms:source ?urn .
  BIND (IRI(CONCAT(str(?urn), "&role=image&size=variable")) AS ?image)

  OPTIONAL {
   ?photo dc:title ?title ;
    dc:description ?description ;
    dcterms:extent ?extent .
  }
}
LIMIT 100"""

SPARQL_QUERY_2 = """PREFIX wdt: <http://www.wikidata.org/property/> SELECT ?rijksmonument ?nummer WHERE {?rijksmonument wdt:P359 ?nummer; wdt:P131 wd:Q9899; rdfs:label "{0}"@nl.} LIMIT 1000"""

async def prenten(request):
    sparql = SPARQLWrapper(SPARQL_URI,returnFormat=JSON)
    sparql.addDefaultGraph("http://lod.kb.nl/gvn/ubl01/")
    sparql.setQuery(SPARQL_QUERY)
    res = sparql.query()
    return web.json_response(data=res.convert())


async def monumenten(request):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql", returnFormat=JSON)
    sparql.setQuery(SPARQL_QUERY_2.format("Oude Kerk"))
    res = sparql.query()
    return web.json_response(data=res.convert())


async def monument(request):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql", returnFormat=JSON)
    sparql.setQuery(SPARQL_QUERY_2.format(request.match_info['gebouw']))
    res = sparql.query()
    return web.json_response(data=res.convert())

app = web.Application()
app.router.add_get('/', prenten)
app.router.add_get('/gebouw', monumenten)
resource = app.router.add_resource('/gebouw/{gebouw}')
resource.add_route('GET', monument)


web.run_app(app, port=5000)
