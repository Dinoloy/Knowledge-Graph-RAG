
import csv
from collections import Counter

with open("department_audit.csv", encoding="utf-8-sig", newline="") as file:
    rows = list(csv.DictReader(file))

counts = Counter(
    row["Extracted Department"].strip() or "[BLANK]"
    for row in rows
)

print("Total records:", len(rows))
print("\nDepartment counts:")

for department, count in counts.most_common():
    print(f"{department}: {count}")

print("\nFirst 10 schemes:")

for row in rows[:10]:
    print(f'{row["Scheme Name"]} -> {row["Extracted Department"]}')
