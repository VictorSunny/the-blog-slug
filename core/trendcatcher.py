import os
from decouple import config
import requests
import json
from datetime import datetime, timedelta
from blogslug import settings

api_key = config("WORLD_NEWS_API_KEY")

# BASE_DIR = Path(__file__).resolve().parent

def datafetcher(request):
    """"
        provides news data sourced from worldnewsapi.
        handles caching, updating, and serving news content based on user authentication level.
    """

    ### RETURN NEWS DATA FOR TESTING ###
    ### UNHASH THE FOLLOWING "IF" BLOCK BEFORE CARRYING OUT TESTS, HASH OUT AFTER CARRYING OUT TESTS ###
    ###  USE TO AVOID RAISING CONNECTION ERROR, OR CONNECT GET CONNECTED TO THE INTERNET ###

    # if settings.DEBUG == True:
    #     with open("core/data/test_user_news_data/test_news_data.json", "r", encoding= "utf-8") as news_data:
    #         test_news_json = json.load(news_data)
    #     return test_news_json


    # api request header
    headers = {"Content-type": "application/json", "x-api-key": api_key}

    yday = datetime.today() - timedelta(days= 1)
    yesterday = datetime.strftime(yday, "%Y-%m-%d")

    # file location string for local news data for anonymous user
    local_json_file = BASE_DIR / "core/data/anonymous_user_news/anon_news_data.json"

    # validity period in hours before news dictionary is updated through api
    hours_before_refresh = config("NEWS_REFRESH_INTERVAL", cast= int)

    ### CHECK IF USER IS LOGGED IN TO DETERMINE WHAT NEWS DATA TO SERVE

    # if user is logged in, attempt to retrieve news data from user data
    # if user is not logged in, attempt to retieve news data from file folder
    if request.user.is_authenticated:
        news_json = request.user.personalized_articles

        if news_json == "null":
            news_json = None
        
        # set source country variable using user data for api call query
        source_country = request.user.nationality.code.lower()
        print(f"{news_json};   logged in")
    else:
        try:
            with open(local_json_file, "r", encoding= "utf-8") as data:
                news_json = json.load(data)
        except (FileNotFoundError, json.JSONDecodeError):
            news_json = None

        # set source country variable as blank for api call query
        # api will use default source=country value where none is given
        source_country = ""

    ### CHECK IF NEWS DATA EXISTS

    # if news data exists
    if news_json != None :
        date_updated = datetime.strptime(news_json["date_updated"], "%Y-%m-%d %H:%M:%S.%f")

        # check if news data has reached expiry date
        # if expired, delete news data and call function recursively to restart
        if datetime.now() > (date_updated + timedelta(hours= hours_before_refresh)):
            print("deleting outdated news dictionary...")
            if not request.user.is_authenticated:
                os.remove(local_json_file)
            else:
                user = request.user
                user.personalized_articles = None
                user.save()
            print("outdated news dictionary deleted")

            return datafetcher(request)
        else:
            # print(f"date update: {date_updated}\ntoday's date: {datetime.now()}")
            print(f"retrieving news dictionary\nnews json validity: {round(((date_updated + timedelta(hours= hours_before_refresh)) - datetime.now()).total_seconds() / 3600)} hours left")
            return news_json

    # if news data does not exist, request news data from api    
    else:

        # api call to retrieve news data
        news = requests.get(
            url= f"https://api.worldnewsapi.com/search-news?earliest-publish-date={yesterday}&source-country={source_country}&language=en",
            headers= headers,
        )

        # create new key-value pair "date_updated" inside api-retrieved news json
        # "date_updated" variable will be used to check if news data is valid or expired when compared to expected expiry date
        news_data = news.json()
        news_data["date_updated"] = str(datetime.now())

        date_updated = datetime.strptime(news_data["date_updated"], "%Y-%m-%d %H:%M:%S.%f")
        print(f"retrieving news dictionary\nnews json validity: {round(((date_updated + timedelta(hours= hours_before_refresh)) - datetime.now()).total_seconds() / 3600)} hours left")

        # if user is logged in, retrieve news data from user data and return
        # if user is not logged in, retieve news data from file folder and return
        if request.user.is_authenticated:
            request.user.personalized_articles = news_data
            request.user.save()
            return request.user.personalized_articles
        else:
            print("anon user")
            with open(local_json_file, "w", encoding= "utf-8") as news_json:
                json.dump(news_data, news_json, ensure_ascii= False)

            with open(local_json_file, "r", encoding= "utf-8") as news:
                news_json = json.load(news)
            return news_json



