import pandas as pd
import json

url = "https://docs.google.com/spreadsheets/d/1RB9rxbcQ5B4RAIuXxymZKD64hRhdsWw1-SuN6GyEG_4/export?format=csv&gid=1907582977"
df = pd.read_csv(url, header=None).fillna("")

def clean_number(value):
    text = str(value).strip()

    if text in ("", "-", "—", "#DIV/0!", "#N/A", "#VALUE!", "nan"):
        return 0.0

    text = text.replace("R", "").replace(",", "").replace(" ", "")
    is_percent = "%" in text
    text = text.replace("%", "")

    if text in ("", "-", "—"):
        return 0.0

    try:
        number = float(text)
        return number / 100 if is_percent else number
    except:
        return 0.0

consultants = []

# Based on your current sheet shape:
# col 1 = name, col 4/5/6 = Apr/May/Jun, col 7 = actual, col 8 = target, col 9 = pct
for i in range(5, 30):
    name = str(df.iloc[i, 1]).strip()
    if not name or name == "0":
        continue

    actual = clean_number(df.iloc[i, 7])
    target = clean_number(df.iloc[i, 8])
    pct = clean_number(df.iloc[i, 9])

    monthly_target = target / 3 if target else 0.0
    gap = target - actual if target else 0.0

    if pct >= 1.0:
        band = "Over target"
    elif pct >= 0.6:
        band = "On track"
    elif pct > 0:
        band = "Build mode"
    else:
        band = "Starting blocks"

    consultants.append({
        "name": name,
        "apr": clean_number(df.iloc[i, 4]),
        "may": clean_number(df.iloc[i, 5]),
        "jun": clean_number(df.iloc[i, 6]),
        "actual": actual,
        "target": target,
        "pct": pct,
        "gap": gap,
        "band": band
    })

team_actual = sum(c["actual"] for c in consultants)
team_target = sum(c["target"] for c in consultants)

data = {
    "summary": {
        "team_actual": team_actual,
        "team_target": team_target,
        "team_pct": (team_actual / team_target) if team_target else 0.0,
        "team_gap": team_target - team_actual,
        "active_consultants": sum(1 for c in consultants if c["actual"] > 0),
        "consultant_count": len(consultants)
    },
    "consultants": consultants
}

with open("s4cloud_sales_kpi_dashboard_v2_data.json", "w") as f:
    json.dump(data, f)

print("Data updated from Google Sheets")
