import pandas as pd
import json

# Load Excel
xls = pd.ExcelFile("S4Cloud Tracker FY27.xlsx")

# Read main sheet
df = pd.read_excel(xls, sheet_name="Consultant NFI League")

# Clean basic data
df = df.fillna(0)

consultants = []

for i in range(5, 30):
    name = df.iloc[i,1]
    if not name:
        continue
    
    consultants.append({
        "name": str(name),
        "actual": float(df.iloc[i,7] or 0),
        "target": float(df.iloc[i,8] or 0),
        "pct": float(df.iloc[i,9] or 0)
    })

data = {
    "consultants": consultants
}

# Write JSON used by dashboard
with open("s4cloud_sales_kpi_dashboard_v2_data.json", "w") as f:
    json.dump(data, f)

print("Data updated from Excel")
