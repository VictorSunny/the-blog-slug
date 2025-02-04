import requests
from bs4 import BeautifulSoup

def datafetcher():
    url = "https://punchng.com/all-posts/"
    raw_news = requests.get(url=url).text.encode("ascii", "ignore")
    news_html = BeautifulSoup(raw_news)
    headlines = news_html.find_all("h1", "post-title")[1:]
    news_images = news_html.find_all("a", "post-image")[1:]

    news_headlines = []
    news_links = []
    for headline in headlines:
        news_headlines.append(headline.string)
        news_links.append(headline.find("a").get("href"))

    article_dict = {"mains": []}
    for intro, link in zip(news_headlines, news_links):
        dictionary = {"headline": intro, "link": link}
        article_dict["mains"].append(dictionary)
    return  article_dict