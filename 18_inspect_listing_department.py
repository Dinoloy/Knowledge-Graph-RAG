
import requests
from bs4 import BeautifulSoup

url = "https://www.tn.gov.in/scheme_list.php?dep_id=Mg=="

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30,
)

print("HTTP status:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

print("\nPage title:")
print(soup.title.get_text(" ", strip=True) if soup.title else "No title")

print("\nDepartment-related text:")
for text in soup.find_all(string=lambda value: value and "department" in value.lower()):
    cleaned = " ".join(text.strip().split())
    if cleaned:
        print(cleaned[:300])

print("\nFirst 15 scheme links:")
count = 0

for link in soup.find_all("a", href=True):
    href = link["href"]
    name = link.get_text(" ", strip=True)

    if "scheme_details.php" in href and name:
        print(f"{name} -> {href}")
        count += 1

        if count >= 15:
            break
