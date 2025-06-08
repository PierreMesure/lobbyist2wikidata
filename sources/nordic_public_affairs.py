import requests
from bs4 import BeautifulSoup

URL = "https://nordicpa.se/medarbetare/"

def get_content():
    """
    Fetches a webpage and extracts the name and text.
    """
    try:
        response = requests.get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        entries = soup.find_all("article", class_="preview-employee")
        for entry in entries:
            name_tag = entry.find("h2", class_="preview-title")
            name = name_tag.get_text(strip=True) if name_tag else None
            text_div = entry.find("div", class_="entry-content")
            text = text_div.get_text(strip=True) if text_div else None
            if name and text:
                print(f"Name: {name}")
                print(f"Text: {text}")
                print("-" * 20)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching content for {URL}: {e}")
        return {"name": None, "text": None}


if __name__ == "__main__":
    get_content()
