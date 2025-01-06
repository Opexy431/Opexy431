import requests

def fetch_wikipedia_article(title):
    url = f"https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts",
        "explaintext": True,
        "redirects": 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    page = next(iter(data['query']['pages'].values()))
    return page.get('extract', 'Article not found.')

# Example usage
article_title = "Music"
article_content = fetch_wikipedia_article(article_title)
print(article_content)
