
import requests
from bs4 import BeautifulSoup

# Official Tamil Nadu government schemes webpage
URL = "https://www.tn.gov.in/scheme_list.php?dep_id=Mg=="


def load_document(url):
    """Fetch and extract readable text from a webpage."""
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unnecessary page elements
    for element in soup(["script", "style", "nav", "footer"]):
        element.decompose()

    text = soup.get_text(separator="\n", strip=True)

    return text


if __name__ == "__main__":
    try:
        document = load_document(URL)

        print("Document loaded successfully!")
        print(f"Total characters: {len(document)}")
        print("\nFirst 2000 characters:\n")
        print(document[:2000])

        # Save the extracted text
        with open("schemes_data.txt", "w", encoding="utf-8") as file:
            file.write(document)

        print("\nSaved extracted text to schemes_data.txt")

    except requests.RequestException as error:
        print(f"Error fetching webpage: {error}")
