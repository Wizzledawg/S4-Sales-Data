import pandas as pd
import json

url = "https://docs.google.com/spreadsheets/d/1RB9rxbcQ5B4RAIuXxymZKD64hRhdsWw1-SuN6GyEG_4/export?format=csv&gid=1907582977"
df = pd.read_csv(url).fillna("")

def clean_number(value):
    if value is None:
        return 0.0

    text = str(value).strip()

    if text in ("", "-", "—", "n/a", "N/A", "#DIV/0!", "#N/A", "#VALUE!", "#REF!"):
        return 0.0

    text = text.replace("R", "").replace(",", "").replace(" ", "")
    is_percent = "%" in text
    text = text.replace("%", "")

    if text in ("", "-", "—"):
        return 0.0

    number = float(text)
    return number / 100 if is_percent else number

consultants = []

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
        "business": "Smart4 Cloud",
        "type": "Consultant",
        "apr": clean_number(df.iloc[i, 4]),
        "may": clean_number(df.iloc[i, 5]),
        "jun": clean_number(df.iloc[i, 6]),
        "actual": actual,
        "target": target,
        "pct": pct,
        "monthly_target": monthly_target,
        "gap": gap,
        "band": band,
        "live_contracts": 0,
        "contract_gp_pm": 0
    })

team_actual = sum(c["actual"] for c in consultants)
team_target = sum(c["target"] for c in consultants)
team_pct = (team_actual / team_target) if team_target else 0.0

data = {
    "summary": {
        "team_actual": team_actual,
        "team_target": team_target,
        "team_pct": team_pct,
        "team_gap": team_target - team_actual,
        "energy_actual": 0,
        "cloud_actual": team_actual,
        "perm_actual": 0,
        "contract_actual": 0,
        "active_consultants": sum(1 for c in consultants if c["actual"] > 0),
        "consultant_count": len(consultants),
        "avg_nfi_per_consultant": (team_actual / len(consultants)) if consultants else 0,
        "monthly_actuals": {
            "Apr": sum(c["apr"] for c in consultants),
            "May": sum(c["may"] for c in consultants),
            "Jun": sum(c["jun"] for c in consultants)
        },
        "monthly_target": {
            "Apr": sum(c["monthly_target"] for c in consultants),
            "May": sum(c["monthly_target"] for c in consultants),
            "Jun": sum(c["monthly_target"] for c in consultants)
        },
        "live_contractors": 0,
        "live_gp_pm": 0,
        "perm_placements": 0
    },
    "consultants": consultants,
    "topClients": [],
    "contractorBook": [],
    "permPlacements": []
}

with open("s4cloud_sales_kpi_dashboard_v2_data.json", "w") as f:
    json.dump(data, f)

print("Data updated from Google Sheets")
