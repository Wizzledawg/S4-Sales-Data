import pandas as pd
import json

url = "https://docs.google.com/spreadsheets/d/1RB9rxbcQ5B4RAIuXxymZKD64hRhdsWw1-SuN6GyEG_4/export?format=csv&gid=1907582977"
df = pd.read_csv(url)

# Clean column names
df.columns = [c.strip().lower() for c in df.columns]

def clean_number(value):
    if pd.isna(value):
        return 0.0

    text = str(value).strip()

    if text in ("", "-", "—", "#DIV/0!", "#N/A", "#VALUE!"):
        return 0.0

    text = text.replace("R", "").replace(",", "").replace(" ", "")
    is_percent = "%" in text
    text = text.replace("%", "")

    try:
        num = float(text)
        return num / 100 if is_percent else num
    except:
        return 0.0

# 🔥 Map your ACTUAL column names here (adjust once, then stable forever)
NAME_COL = "consultant"
APR_COL = "apr"
MAY_COL = "may"
JUN_COL = "jun"
ACTUAL_COL = "actual"
TARGET_COL = "target"
PCT_COL = "pct"

consultants = []

for _, row in df.iterrows():
    name = str(row.get(NAME_COL, "")).strip()
    if not name or name.lower() in ["total", ""]:
        continue

    actual = clean_number(row.get(ACTUAL_COL))
    target = clean_number(row.get(TARGET_COL))
    pct = clean_number(row.get(PCT_COL))

    monthly_target = target / 3 if target else 0
    gap = target - actual if target else 0

    if pct >= 1:
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
        "apr": clean_number(row.get(APR_COL)),
        "may": clean_number(row.get(MAY_COL)),
        "jun": clean_number(row.get(JUN_COL)),
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

data = {
    "summary": {
        "team_actual": team_actual,
        "team_target": team_target,
        "team_pct": team_actual / team_target if team_target else 0,
        "team_gap": team_target - team_actual,
        "active_consultants": sum(1 for c in consultants if c["actual"] > 0),
        "consultant_count": len(consultants)
    },
    "consultants": consultants
}

with open("s4cloud_sales_kpi_dashboard_v2_data.json", "w") as f:
    json.dump(data, f)

print("✅ Data rebuilt correctly")
