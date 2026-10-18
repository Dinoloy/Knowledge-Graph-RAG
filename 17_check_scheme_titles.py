
import json

with open("schemes_details.json", encoding="utf-8") as file:
    records = json.load(file)

print("Checking the first 10 scheme records:\n")

for record in records[:10]:
    details = record.get("details", {})

    listed_name = record.get("scheme_name", "")
    detail_title = details.get("Scheme Title/Name", "")

    print("Listing name:", listed_name)
    print("Detail title:", detail_title)
    print("Department:", details.get("Concerned Department", ""))
    print("-" * 60)
