
import json
import time
import requests
from bs4 import BeautifulSoup

INPUT_FILE = "schemes_list.json"
OUTPUT_FILE = "schemes_details.json"

BASE_URL = "https://www.tn.gov.in/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 Chrome/131.0 Safari/537.36"
}

FIELD_LABELS = [
    "Concerned Department",
    "Concerned District",
    "Organisation Name",
    "Scheme Title/Name",
    "Associated Scheme",
    "Sponsered By",
    "Funding Pattern",
    "Beneficiaries",
    "Types of Benefits",
    "Eligibility criteria",
    "Income",
    "Age From",
    "Age To",
    "Community",
    "How To avail",
    "Validity of the Scheme",
    "Introduced On",
    "Description",
    "Scheme Type",
    "Uploaded File",
]


def clean_text(text):
    return " ".join(text.split()).strip()


def extract_details(url):
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for element in soup(["script", "style", "nav", "footer"]):
        element.decompose()

    # Extract text from table cells and page content.
    # Preserve line breaks so field labels can be identified.
    for br in soup.find_all("br"):
        br.replace_with("\n")

    page_text = soup.get_text("\n", strip=True)
    lines = [
        line.strip()
        for line in page_text.splitlines()
        if line.strip()
    ]

    details = {label: "" for label in FIELD_LABELS}

    # Find each field label and collect its value until
    # the next known field label.
    normalized_labels = {
        label.lower(): label for label in FIELD_LABELS
    }

    i = 0
    while i < len(lines):
        current = lines[i].strip().rstrip(":").strip()
        label = normalized_labels.get(current.lower())

        if not label:
            i += 1
            continue

        values = []
        j = i + 1

        while j < len(lines):
            next_line = lines[j].strip().rstrip(":").strip()

            if next_line.lower() in normalized_labels:
                break

            values.append(lines[j].strip())
            j += 1

        details[label] = "\n".join(values).strip()
        i = j

    return details


with open(INPUT_FILE, "r", encoding="utf-8") as file:
    schemes = json.load(file)

results = []
successful = 0
failed = 0

for index, scheme in enumerate(schemes, start=1):
    name = scheme.get("scheme_name", "")
    url = scheme.get("url", "")

    print(f"[{index}/{len(schemes)}] Extracting: {name}")

    try:
        details = extract_details(url)

        results.append({
            "scheme_name": name,
            "url": url,
            "details": details,
            "error": "",
        })

        successful += 1

        print(
            "  Department:",
            details.get("Concerned Department") or "[NOT FOUND]"
        )

    except Exception as error:
        print(f"  ERROR: {error}")
        failed += 1

        results.append({
            "scheme_name": name,
            "url": url,
            "details": {},
            "error": str(error),
        })

    time.sleep(0.3)

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(
        results,
        file,
        ensure_ascii=False,
        indent=2,
    )

print("\nExtraction completed!")
print(f"Total schemes: {len(schemes)}")
print(f"Successful: {successful}")
print(f"Failed: {failed}")
print(f"Saved to: {OUTPUT_FILE}")
