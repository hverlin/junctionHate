from webapp.apps.fact_checker.DuckduckgoSearch import DuckduckgoSearch

website_liste = DuckduckgoSearch().search_on_html_duckduckgo("donal trump")
print(len(website_liste))
