from SPARQLWrapper import SPARQLWrapper, JSON


class WikidataQuery:
    def __init__(self):
        self._sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
        self._sparql.setReturnFormat(JSON)

    @staticmethod
    def _extract_qid(url: str) -> str:
        return url.split('/')[-1]

    def _run_query(self, query: str):
        try:
            self._sparql.setQuery(query)
            return self._sparql.query().convert()['results']['bindings']
        except:
            return None

    @staticmethod
    def _get_string(attribute, row):
        return row[attribute]['value']

    @staticmethod
    def _get_qid(attribute, row):
        return WikidataQuery._extract_qid(row[attribute]['value'])

    @staticmethod
    def _get_date(attribute, row):
        raw_date = WikidataQuery._get_string(attribute, row)

        return raw_date[:10]

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

        politicians = self._run_query(query)

        if not politicians:
            return None

        return self._get_string('politicianLabel', politicians[0]),\
            self._get_qid('politician', politicians[0])

    def birthdate(self, qid:str) -> str:
        query = """
            SELECT ?date WHERE {{
                wd:{0} wdt:P569 ?date.
            }}
        """.format(qid)
        results = self._run_query(query)

        if not results:
            return None

        return self._get_date('date', results[0])
