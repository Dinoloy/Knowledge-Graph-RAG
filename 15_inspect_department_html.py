
import requests
from bs4 import BeautifulSoup

schemes = {
    "Training to Farmers": "https://www.tn.gov.in/scheme_details.php?id=MTU2Ng==",
    "UYEGP": "https://www.tn.gov.in/scheme_details.php?id=MzM=",
    "MSME Technology Development Fund": "https://www.tn.gov.in/scheme_details.php?id=Mjg=",
}

for name, url in schemes.items():
    print("\n" + "=" * 60)
    print("Scheme:", name)

    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30,
    )

    print("HTTP status:", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    for row in soup.find_all("tr"):
        cells = row.find_all("td")

        if len(cells) >= 2:
            label = cells[0].get_text(" ", strip=True)
            value = cells[1].get_text(" ", strip=True)

            if "department" in label.lower() or "scheme title" in label.lower():
                print(f"{label} {value}")
