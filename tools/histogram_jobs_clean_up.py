import pandas as pd
import re

pattern = r"[0-9]{2}.[0-9]{4}.[0-9]{2}"
data = pd.read_csv("jobs_metadata_martin.csv")

liste = data["related_occupations"].iloc[1].split(",")
for x in liste:
    if re.fullmatch(pattern, x):
        print(x)
    else:
        print("false : ", x)
