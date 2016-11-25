import requests
from bs4 import BeautifulSoup


class DuckduckgoSearch():

    def search_on_html_duckduckgo(self, search):
        refactor_search = search.replace (" ", "+")

        request = "https://duckduckgo.com/html/?q="+refactor_search
        result = requests.get(request)
        parsed_html = BeautifulSoup(result.text, 'html.parser')
        link_list = parsed_html.body.find_all('a', attrs={'class': 'result__url'})

        final_website_list = []
        for link in link_list:
            if link.get('href'):
                final_website_list.append(link.get('href'))

        return final_website_list