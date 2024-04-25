import pandas as pd
import requests
import datetime



def data_row_count(endpoint):
    get_request = f'{endpoint}.json?$select=count%28*%29'
    get = requests.get(get_request).json()

    count = get[0]["count"]

    return int(count)





def get_data(endpoint, 
             start = None,
             end = None,
             offset = None, 
             limit = None):
    
    if start is not None:
        if  type(start) is datetime.date:
            s = start.strftime("%Y-%m-%d")
        elif type(start) is datetime.datetime:
            s = start.strftime("%Y-%m-%dT%H:%M:%S")
        else:
            print("Error: The start argument is not a valid date or time object")
            return
    
    if end is not None:
        if  type(end) is datetime.date:
            e = end.strftime("%Y-%m-%d")
        elif type(end) is datetime.datetime:
            e = end.strftime("%Y-%m-%dT%H:%M:%S")
        else:
            print("Error: The end argument is not a valid date or time object")
            return

    q = ""
    c = "?"
    if offset is not None and (start is not None or end is not None):
        print("Warning: Ignoring the offset argument - cannot use the offset argument while using the start or end argument.")
    elif offset is not None:
        q = q +  f"{c}$offset={offset}"
        c = "&"

    if limit is not None:  
         q = q + f"{c}$limit={limit}" 
         c = "&"
    
    if start is not None and end is not None:
        q = q + f"{c}$where=date between '{s}' and '{e}'"
        c = "&"

    if start is not None and end is None:
        q = q + f"{c}$where=date >= '{s}'"
        c = "&"

    if end is not None and start is None:
        q = q + f"{c}$where=date <= '{e}'"
        c = "&"
    
    get_request = f"{endpoint}.json" + q
    get = requests.get(get_request)

    return get


def chicago_data_reformat(json):
    
    columns_list = ['id', 'case_number', 'date', 'block', 'iucr', 'primary_type',
       'description', 'location_description', 'arrest', 'domestic', 'beat',
       'district', 'ward', 'community_area', 'fbi_code', 'x_coordinate',
       'y_coordinate', 'year', 'updated_on', 'latitude', 'longitude']

    d = pd.json_normalize(json.json())[columns_list]
    
    return d



def day_offset(start, end, offset):
    current = [start]
    while max(current) < end:
        if(max(current) + datetime.timedelta(days= offset) < end):
            current.append(max(current) + datetime.timedelta(days= offset))
        else:
           current.append(end) 
           
    return current

def hour_offset(start, end, offset):
    current = [start]
    while max(current) < end:
        if(max(current) + datetime.timedelta(hours = offset) < end):
            current.append(max(current) + datetime.timedelta(hours = offset))
        else:
           current.append(end) 
           
    return current


def offset_vector(start, end, limit):
    class offset_vector():
        def __init__(self, offset, limit):
            self.offset = offset
            self.limit = limit

    v = list(range(start, end))
    l = [limit] * len(v)
    if max(v) > end - limit:
        l[len(l) - 1] = end - max(v)
    output = offset_vector(offset = v, limit = l)
    return output


def backfill_chicago_data(endpoint, start, end, offset, limit = None):
    df = None

    if  type(start) is datetime.date:
        time_vec_seq = day_offset(start = start, end = end, offset = offset)
    elif  type(start) is datetime.datetime:
        time_vec_seq = hour_offset(start = start, end = end, offset = offset)

    for i in range(len(time_vec_seq) - 1):
        s = time_vec_seq[i]
        e = time_vec_seq[i + 1]

        if  type(e) is datetime.datetime:
            e = e - datetime.timedelta(hours = 1)
        elif type(e) is datetime.date:
            e = e - datetime.timedelta(days = 1) 


       
        temp = get_data(endpoint = endpoint, start = s, end = e, limit = limit)
        temp = chicago_data_reformat(temp)
        
        if df is None:
            df = temp
        else:
            df = df._append(temp)

    df["datetime"] = pd.to_datetime(df["date"])
    df = df.sort_values(by = ["datetime"])
    df = df.loc[:, df.columns != "date"]
    first_c_names = ["id", "case_number", "datetime"]
    last_c_names = [c for c in df.columns if c not in first_c_names]
    df.reset_index(drop=True, inplace=True)
    df = df[first_c_names + last_c_names]


    return df
        
