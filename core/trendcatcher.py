import requests
from bs4 import BeautifulSoup

def datafetcher():
    url = "https://punchng.com/all-posts/"
    raw_news = requests.get(url=url).text.encode("ascii", "ignore")

    news_html = BeautifulSoup(raw_news, "html.parser")
    headlines = news_html.find_all("h1", "post-title")
    article_image_urls = news_html.find_all("img", "post-image")
    article_date = news_html.find_all("span", "post-date")


    news_headlines = []
    article_links = []
    dates = []

    for headline in headlines:
        news_headlines.append(headline.string)
        article_links.append(headline.find("a").get("href"))

    for date in article_date:
        stripped_date = date.get_text()
        dates.append(stripped_date)

    print(dates)

    article_dict = []
    for intro, link, date in zip(news_headlines, article_links, dates):
        dictionary = {"headline": intro, "link": link, "date": date}
        article_dict.append(dictionary)
    return  article_dict

