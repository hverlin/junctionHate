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
        except BaseException as e:
            print(e)
            return None

    @staticmethod
    def _get_string(attribute, row):
        return row[attribute]['value'] if attribute in row else None

    @staticmethod
    def _get_qid(attribute, row):
        return WikidataQuery._extract_qid(row[attribute]['value'])

    @staticmethod
    def _get_date(attribute, row):
        raw_date = WikidataQuery._get_string(attribute, row)

        if not raw_date:
            return None

        return raw_date[8:10] + '/' + raw_date[5:7] + '/' + raw_date[:4]

    def search_politician(self, firstname: str, lastname: str) -> (str, str):
        """
        Search for a politician

        :return: (complete name: str, QID: str) or None
        """
        query = """
            # Find politician by name
            SELECT ?politician ?politicianLabel WHERE {{
              ?politician wdt:P106 wd:Q82955.

              ?politician wdt:P735 [ rdfs:label "{0}"@en].
              ?politician wdt:P734 [ rdfs:label "{1}"@en].

              SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
            }}
            LIMIT 1
            """.format(firstname, lastname)

        politicians = self._run_query(query)

        if not politicians:
            return None

        return self._get_string('politicianLabel', politicians[0]),\
            self._get_qid('politician', politicians[0])

    def birthdate(self, qid:str) -> str:
        """
        Query the birth date of a person.
        :param qid: QID of the person
        :return: The date represented as a string 'dd/MM/YYYY' or None
        """
        query = """
            SELECT ?date WHERE {{
                wd:{0} wdt:P569 ?date.
            }}
        """.format(qid)
        results = self._run_query(query)

        if not results:
            return None

        return self._get_date('date', results[0])

    def image(self, qid:str) -> str:
        """
        Return the URL of the image or None.
        """
        query = """
            SELECT ?image WHERE {{
                wd:{0} wdt:P18 ?image.
            }}
        """.format(qid)
        results = self._run_query(query)

        if not results:
            return None

        return self._get_string('image', results[0])

    def official_website(self, qid:str) -> str:
        query = """
            SELECT ?site WHERE {{
                wd:{0} wdt:P856 ?site.
            }}
        """.format(qid)
        results = self._run_query(query)

        if not results:
            return None

        return self._get_string('site', results[0])

    def political_parties(self, qid:str):
        """
        Returns a list of dict (or None):
        {
            'qid': QID of the party
            'name': English name of the party
            'start': Date when entered in the party
            'end': Date when left it (or None if still in it)
        }
        """
        query = """
        SELECT ?party ?partyLabel ?start ?end WHERE {{
          wd:{0} p:P102 ?s.
          ?s ps:P102 ?party.
          ?s pq:P580 ?start.

          OPTIONAL{{
            ?s pq:P582 ?end.
          }}

          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        """.format(qid)
        results = self._run_query(query)

        if not results:
            return None

        return [
            {
                'qid': WikidataQuery._get_qid('party', row),
                'start': WikidataQuery._get_date('start', row),
                'end': WikidataQuery._get_date('end', row),
                'name': WikidataQuery._get_string('partyLabel', row),
            }
            for row in results
        ]

    def awards(self, qid:str):
        """
        Return the awards received by the person.

        Return a list of dict (or None):
        {
            'qid': The QID of the award
            'name': The designation of the award
            'date': The date when the person won the award
        }
        """
        query = """
        SELECT ?award ?awardLabel ?date WHERE {
          wd:Q22686 p:P166 [
              ps:P166 ?award;
              pq:P585 ?date;
          ]

          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        """

        results = self._run_query(query)

        if not results:
            return None

        return [
            {
                'qid': WikidataQuery._get_qid('award', row),
                'name': WikidataQuery._get_string('awardLabel', row),
                'date': WikidataQuery._get_date('date', row)
            }
            for row in results
        ]