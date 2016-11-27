import requests
import re
from bs4 import BeautifulSoup


def search_on_html_duckduckgo(search):
    refactor_search = search.replace (" ", "+")

    request = "https://duckduckgo.com/html/?q="+refactor_search
    result = requests.get(request)
    parsed_html = BeautifulSoup(result.text, 'html.parser')
    link_list = parsed_html.body.find_all('a', attrs={'class': 'result__url'})

    final_website_list = []
    for link in link_list:
        if link.get('href'):
            final_website_list.append(link.get('href'))

    title_list = parsed_html.body.find_all('a', attrs={'class': 'result__a'})
    click_bait = 0
    for a in title_list:
        res = re.search("\d+ ", a.text)
        if res:
            click_bait += 1


    return final_website_list,request,click_bait