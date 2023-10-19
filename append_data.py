import pandas as pd
import os

path = "./data_raw"

files = os.listdir(path = path)

for i in files:
    print(path +"/" + i)

df = pd.concat((pd.read_csv(path +"/" + f) for f in files), ignore_index=True)