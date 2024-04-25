import pandas as pd
import chicago_data
import datetime



# endpoints = {2020: "https://data.cityofchicago.org/resource/qzdf-xmn8",
#              2021: "https://data.cityofchicago.org/resource/dwme-t96c",
#              2022: "https://data.cityofchicago.org/resource/9hwr-2zxp",
#              2023: "https://data.cityofchicago.org/resource/xguy-4ndq",
#              2024: "https://data.cityofchicago.org/resource/dqcy-ctma"}


endpoint = "https://data.cityofchicago.org/resource/ijzp-q8t2"



start = datetime.datetime(2020,1,1,0,0,0)
end = datetime.datetime(2024,4,24,0,0,0)
df = chicago_data.backfill_chicago_data(endpoint = endpoint, 
                                       start = start, 
                                       end = end, 
                                       offset = 24 * 30,
                                       limit = 100000)


df.to_csv("data/chicago_crime_2020-2024.csv", index = False)
