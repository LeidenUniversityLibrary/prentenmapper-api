# Wrapper voor SPARQL-query's
import urllib.parse

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

SPARQL_QUERY_2 = '''SELECT ?rijksmonument ?nummer ?coordinates ?street 
WHERE {{?rijksmonument wdt:P359 ?nummer; wdt:P131 wd:Q9899; rdfs:label "{0}"@nl; wdt:P625 ?coordinates. 
OPTIONAL {{?rijksmonument wdt:P669 ?street.}} }} 
LIMIT 1000'''

SPARQL_CONSTRUCT = '''CONSTRUCT {{
  ?rijksmonument wdt:P359 ?nummer;
                 wdt:P625 ?coordinates;
                 wdt:P669 ?street }}
WHERE 
{{?rijksmonument wdt:P359 ?nummer; 
                wdt:P131 wd:Q9899; 
                rdfs:label "{0}"@nl; 
                wdt:P625 ?coordinates. 
 OPTIONAL {{?rijksmonument wdt:P669 ?street.}} }}
LIMIT 1000'''

async def prenten(request):
    sparql = SPARQLWrapper(SPARQL_URI,returnFormat=JSON)
    sparql.addDefaultGraph("http://lod.kb.nl/gvn/ubl01/")
    sparql.setQuery(SPARQL_QUERY)
    res = sparql.query()
    return web.json_response(data=res.convert())


async def monumenten(request):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql", returnFormat=JSON)
    sparql.setQuery(SPARQL_QUERY_2)
    res = sparql.query()
    return web.json_response(data=res.convert())


async def monument(request):
    term = urllib.parse.unquote(request.match_info['gebouw'])
    print(term)
    if term in request.app['gebouwen_cache']:
        return web.json_response(data=request.app['gebouwen_cache'][term])
    else:
        sparql = request.app['wikidata_sparql']
        sparql.setQuery(SPARQL_QUERY_2.format(term))
        res = sparql.queryAndConvert()
        request.app['gebouwen_cache'][term] = res
        return web.json_response(data=res)


def load_mapping():
    g = rdflib.Graph()
    g.parse('gebouwen.ttl', format='n3')
    print("Loaded graph from gebouwen.ttl:", len(g), "statements")
    return g


async def on_shutdown(app):
    g = app['gebouwen']
    g.serialize('gebouwen.ttl', format='n3')
    print("Stored graph in gebouwen.ttl:", len(g), "statements")


app = web.Application()
app['wikidata_sparql'] = SPARQLWrapper("https://query.wikidata.org/sparql", returnFormat=JSON)
app['gebouwen'] = load_mapping()
app['gebouwen_cache'] = {}
app.router.add_get('/', prenten)
app.router.add_get('/gebouw', monumenten)
resource = app.router.add_resource('/gebouw/{gebouw}')
resource.add_route('GET', monument)

app.on_shutdown.append(on_shutdown)

web.run_app(app, port=5000)
