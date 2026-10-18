
import json

INPUT_FILE = "schemes_details.json"
OUTPUT_FILE = "rag_documents.json"

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    schemes = json.load(file)

documents = []

for record in schemes:
    details = record.get("details", {})

    content = f"""
Scheme Name: {record.get('scheme_name', '')}
Department: {details.get('Concerned Department', '')}
Beneficiaries: {details.get('Beneficiaries', '')}
Benefit Type: {details.get('Types of Benefits', '')}
Funding Pattern: {details.get('Funding Pattern', '')}
Eligibility Criteria: {details.get('Eligibility criteria', '')}
Application Process: {details.get('How To avail', '')}
Description: {details.get('Description', '')}
Source URL: {record.get('url', '')}
""".strip()

    documents.append({
        "id": f"scheme_{len(documents) + 1}",
        "scheme_name": record.get("scheme_name", ""),
        "content": content,
        "source": record.get("url", ""),
    })

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(documents, file, ensure_ascii=False, indent=2)

print("RAG documents prepared successfully!")
print(f"Total documents: {len(documents)}")
print(f"Saved to: {OUTPUT_FILE}")

print("\nFirst document preview:\n")
print(documents[0]["content"][:1500])
