import pandas as pd
import json

url = "https://docs.google.com/spreadsheets/d/1RB9rxbcQ5B4RAIuXxymZKD64hRhdsWw1-SuN6GyEG_4/export?format=csv&gid=1907582977"
df = pd.read_csv(url)

df = df.fillna("")

def clean_number(value):
    if value is None or value == "":
        return 0.0

    text = str(value).strip()
    text = text.replace("R", "").replace(",", "").replace(" ", "")

    is_percent = "%" in text
    text = text.replace("%", "")

    if text == "":
        return 0.0

    number = float(text)

    if is_percent:
        return number / 100

    return number

consultants = []

for i in range(5, 30):
    name = str(df.iloc[i, 1]).strip()
    if not name:
        continue

    consultants.append({
        "name": name,
        "actual": clean_number(df.iloc[i, 7]),
        "target": clean_number(df.iloc[i, 8]),
        "pct": clean_number(df.iloc[i, 9])
    })

data = {
    "consultants": consultants
}

with open("s4cloud_sales_kpi_dashboard_v2_data.json", "w") as f:
    json.dump(data, f)

print("Data updated from Google Sheets")
