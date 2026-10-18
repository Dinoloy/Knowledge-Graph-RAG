
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.tn.gov.in/"
LIST_URL = "https://www.tn.gov.in/scheme_list.php?dep_id=Mg=="

headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(LIST_URL, headers=headers, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

schemes = []

for link in soup.find_all("a", href=True):
    name = link.get_text(" ", strip=True)
    href = link["href"]

    if "scheme_details.php?id=" in href and name:
        schemes.append({
            "scheme_name": name,
            "url": urljoin(BASE_URL, href)
        })

# Remove duplicate URLs
unique_schemes = {
    scheme["url"]: scheme for scheme in schemes
}

schemes = list(unique_schemes.values())

with open("schemes_list.json", "w", encoding="utf-8") as file:
    json.dump(schemes, file, ensure_ascii=False, indent=2)

print(f"Total unique schemes extracted: {len(schemes)}")
print("\nFirst 5 schemes:")

for scheme in schemes[:5]:
    print(scheme["scheme_name"], "->", scheme["url"])

print("\nSaved data to schemes_list.json")
