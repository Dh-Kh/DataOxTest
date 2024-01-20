import pandas as pd
import re
def preprocessing():
    df = pd.read_csv("car_data.csv")
    df["price_usd"] = df["price_usd"].replace('[\$,]', '', regex=True).str.replace(' ', '').astype(int)
    df["odometer"] = df["odometer"].astype(int) * 1000
    df["images_count"] = df["images_count"].apply(
        lambda x: int(re.search(r'\d+', str(x)).group()) if re.search(r'\d+', str(x)) else None).astype(int)
    df.to_csv("car_data.csv", index=False)

