#!/usr/bin/env python3
"""Generate GoalMain CSV from FactMain source data"""

import csv
import os
from datetime import datetime

# Input/output files
input_file = r"C:\Users\PHUyJo3\OneDrive - NESTLE\Documents\projects\data\iowa\Iowa Liquor Sales (Jan 2021-Jan 2022).csv"
output_file = r"C:\Users\PHUyJo3\OneDrive - NESTLE\Documents\projects\iowa\data\GoalMain.csv"

print(f"Reading: {input_file}")

# Read the CSV
rows = []
fieldnames = []
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

print(f"Loaded {len(rows)} rows")

# Find max bottles for variance calculation
max_bottles = 0
for row in rows:
    try:
        bottles = float(row.get('bottles_sold', 0))
        if bottles > max_bottles:
            max_bottles = bottles
    except:
        pass

# Process rows and add goal columns
goal_rows = []
for row in rows:
    try:
        bottles = float(row.get('bottles_sold', 0))
        sale_dollars = float(row.get('sale_dollars', 0))
        volume_liters = float(row.get('volume_sold_liters', 0))
        volume_gallons = float(row.get('volume_sold_gallons', 0))
        
        # Calculate variance: -9% to +5% based on bottles sold percentage
        if max_bottles > 0:
            bottles_pct = bottles / max_bottles
        else:
            bottles_pct = 0.5
            
        variance = -0.09 + (bottles_pct * 0.14)  # Maps 0-100% to -9% to +5%
        variance = max(-0.09, min(0.05, variance))  # Clamp to range
        
        # Create goal values
        goal_row = row.copy()
        goal_row['bottles_sold_goal'] = str(int(bottles * (1 + variance)))
        goal_row['sale_dollars_goal'] = str(round(sale_dollars * (1 + variance), 2))
        goal_row['volume_sold_liters_goal'] = str(round(volume_liters * (1 + variance), 4))
        goal_row['volume_sold_gallons_goal'] = str(round(volume_gallons * (1 + variance), 4))
        
        goal_rows.append(goal_row)
    except Exception as e:
        print(f"  Warning: {e}")
        goal_rows.append(row)

# Update fieldnames to include new columns
new_fields = fieldnames + [
    'bottles_sold_goal',
    'sale_dollars_goal', 
    'volume_sold_liters_goal',
    'volume_sold_gallons_goal'
]

# Create output directory
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Write CSV
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=new_fields)
    writer.writeheader()
    writer.writerows(goal_rows)

print(f"\n✓ Success! Exported to: {output_file}")
print(f"  Rows: {len(goal_rows):,}")
print(f"  Columns: {len(new_fields)}")
print(f"\nNew goal columns added:")
print(f"  • bottles_sold_goal (variance: -9% to +5% based on volume)")
print(f"  • sale_dollars_goal")
print(f"  • volume_sold_liters_goal")
print(f"  • volume_sold_gallons_goal")
