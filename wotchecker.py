import requests


class WoTResult:
    def __init__(self, json):
        self.target = json['target']
        self.reputation = json["0"][0]
        self.trustworthiness = json["0"][1]
        categories = json['categories']

        def test_category(code: str) -> bool:
            return code in categories and categories[code] >= 20

        self.marked_positive = test_category("501")
        self.malware = test_category("101")
        self.phishing = test_category("103")
        self.scam = test_category("104")
        self.potentially_illegal = test_category("105")

        self.misleading_or_unethical = test_category("201")
        self.privacy_risk = test_category("202")
        self.suspicious = test_category("203")
        self.hate = test_category("204")
        self.spam = test_category("205")
        self.pup = test_category("206")

        self.alternative_or_controversial_medecine = test_category("302")

    def is_negative(self) -> bool:
        return (
            self.hate or
            self.malware or
            self.phishing or
            self.scam or
            self.potentially_illegal or
            self.misleading_or_unethical or
            self.privacy_risk or
            self.suspicious or
            self.hate or
            self.spam or
            self.pup or
            self.reputation <= 40
        )

    def is_positive(self):
        return self.marked_positive and self.reputation >= 60 and self.trustworthiness >= 20

    def is_undefined(self):
        return not self.is_positive() and not self.is_negative()


class WoTChecker:
    def __init__(self):
        self._private_key = 'f4c9175c272adff6de0e968cecfebb51d0acbf83'
        self._api_url = 'http://api.mywot.com/0.4/public_link_json2'

    def test_websites(self, *hosts: str):
        """
        Query Web of Trust API for given websites
        :param hosts: URLs to query about
        :return: a list of WoTResult objects (one for each URL). Can be empty
        """
        hosts = ''.join(map(lambda s: s + '/', hosts))

        params = {
            'hosts': hosts,
            'key': self._private_key
        }
        result = requests.get(self._api_url, params=params)

        if result.ok:
            content = result.json()
            return [WoTResult(v) for v in content.values() if '0' in v]

        return []

