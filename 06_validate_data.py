
import json

with open("schemes_details.json", "r", encoding="utf-8") as file:
    schemes = json.load(file)

fields = [
    "Concerned Department",
    "Beneficiaries",
    "Types of Benefits",
    "Funding Pattern",
    "Eligibility criteria",
    "How To avail",
    "Description",
]

print(f"Total scheme records: {len(schemes)}")

print("\nNon-empty field counts:")

for field in fields:
    count = sum(
        bool(record.get("details", {}).get(field, "").strip())
        for record in schemes
    )
    print(f"{field}: {count}/{len(schemes)}")

print("\nSample scheme:")
sample = schemes[0]

print("Name:", sample["scheme_name"])
print("URL:", sample["url"])

for field in fields:
    value = sample.get("details", {}).get(field, "")
    print(f"\n{field}:")
    print(value if value else "[No information found]")
