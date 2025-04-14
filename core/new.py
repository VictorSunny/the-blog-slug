import pandas
from datetime import datetime, timedelta

json_file = "core/data/anonymous_news/dd.json"

str_date = "2025-04-10 14:25:38.466581"

print( datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f") + timedelta(hours= 2) )