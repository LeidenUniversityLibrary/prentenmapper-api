# Wrapper voor SPARQL-query's

from aiohttp import web
import requests

SPARQL_URI = "http://lod.kb.nl/sparql"
SPARQL_QUERY = """
select ?photo ?title ?description ?place ?extent ?image
FROM NAMED <http://lod.kb.nl/gvn/ubl01/>
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

async def hello(request):
    resp = requests.get("http://lod.kb.nl/sparql?default-graph-uri=http%3A%2F%2Flod.kb.nl%2Fgvn%2Fubl01%2F&query=select+%3Fphoto+%3Ftitle+%3Fdescription+%3Fplace+%3Fextents+%3Fimage%0D%0A%23FROM+NAMED+%3Chttp%3A%2F%2Flod.kb.nl%2Fgvn%2Fubl01%2F%3E%0D%0Awhere+%7B%0D%0A++%3Fphoto+a+dctype%3AStillImage+%3B%0D%0A++++dcterms%3Aspatial+%3Fplace+.%0D%0A++FILTER%28REGEX%28%3Fplace%2C+%22Amsterdam%22%29%29%0D%0A%0D%0A++%3Fphoto+dcterms%3Asource+%3Furn+.%0D%0A++BIND+%28IRI%28CONCAT%28str%28%3Furn%29%2C+%22%26role%3Dimage%26size%3Dvariable%22%29%29+AS+%3Fimage%29%0D%0A%0D%0A++OPTIONAL+%7B%0D%0A+++%3Fphoto+dc%3Atitle+%3Ftitle+%3B%0D%0A++++dc%3Adescription+%3Fdescription+%3B%0D%0A++++dcterms%3Aextent+%3Fextents+.%0D%0A++%7D%0D%0A%7D%0D%0ALIMIT+100&format=application%2Fsparql-results%2Bjson&timeout=180000&debug=on&run=+Run+Query+")
    return web.json_response(data=resp.json())


app = web.Application()
app.router.add_get('/', hello)


web.run_app(app, port=5000)
