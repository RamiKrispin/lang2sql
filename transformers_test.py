import pandas as pd
import duckdb
import time 
import os
import torch
from transformers import pipeline

token = os.getenv('HUGGING_FACE_TOKEN')

# Load the data
path = "./data_raw"
files = [x for x in os.listdir(path = path) if ".csv" in x]
print(files)

chicago_crime = pd.concat((pd.read_csv(path +"/" + f) for f in files), ignore_index=True)
print(chicago_crime.head())

# Functions
def create_message(table_name, query):

    class message:
        def __init__(message, system, user, column_names, column_attr):
            message.system = system
            message.user = user
            message.column_names = column_names
            message.column_attr = column_attr

    
    system_template = """

    Given the following SQL table, your job is to write queries given a user’s request. \n

    CREATE TABLE {} ({}) \n
    """

    user_template = "Write a SQL query that returns - {}"
    
    tbl_describe = duckdb.sql("DESCRIBE SELECT * FROM " + table_name +  ";")
    col_attr = tbl_describe.df()[["column_name", "column_type"]]
    col_attr["column_joint"] = col_attr["column_name"] + " " +  col_attr["column_type"]
    col_names = str(list(col_attr["column_joint"].values)).replace('[', '').replace(']', '').replace('\'', '')

    system = system_template.format(table_name, col_names)
    user = user_template.format(query)

    m = message(system = system, user = user, column_names = col_attr["column_name"], column_attr = col_attr["column_type"])
    return m


def add_quotes(query, col_names):
    for i in col_names:
        if i in query:
            query = str(query).replace(i, '"' + i + '"') 
    return(query)

# Set the query

query = "How many cases ended up with arrest?"
msg = create_message(table_name = "chicago_crime", query = query)


m = create_message(table_name = "chicago_crime", query = query)

messages = [
    {
      "role": "system",
      "content": m.system
    },
    {
      "role": "user",
      "content": m.user
    }
    ]

print(messages)



pipe = pipeline("text-generation", 
                model="HuggingFaceH4/zephyr-7b-alpha", 
                torch_dtype=torch.bfloat16, 
                device_map="auto")

prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature= 0.1, top_k=1, top_p=0.95)


print(outputs[0]["generated_text"])