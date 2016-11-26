from SPARQLWrapper import SPARQLWrapper, JSON


class WikidataQuery:
    def __init__(self):
        self._sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
        self._sparql.setReturnFormat(JSON)

    @staticmethod
    def _extract_qid(url: str) -> str:
        return url.split('/')[-1]

    def search_politician(self, firstname: str, lastname: str) -> (str, str):
        """
        Search for a politician

        :return: (complete name: str, QID: str)
        """
        query = """
            # Find politician by name
            SELECT ?politician ?politicianLabel WHERE {{
              ?politician wdt:P106 wd:Q82955.

              ?politician wdt:P735 [ rdfs:label "{0}"@en].
              ?politician wdt:P734 [ rdfs:label "{1}"@en].

              SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
            }}
            LIMIT 10
            """.format(firstname, lastname)
        self._sparql.setQuery(query)
        results = self._sparql.query().convert()

        politicians = results['results']['bindings']

        if len(politicians) > 0:
            return politicians[0]['politicianLabel']['value'], politicians[0]['politician']['value']

        else:
            return None

