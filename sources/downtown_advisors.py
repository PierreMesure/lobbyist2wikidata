import requests
from bs4 import BeautifulSoup

URL = "https://downtownadvisors.se"


def get_content():
    """
    Fetches a webpage and extracts the name and text.
    """
    try:
        response = requests.get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        entries = soup.find_all("div", class_="dipi-flip-box-inner-wrapper")
        for entry in entries:
            name_tag = entry.find("h2", class_="dipi-flip-box-heading")
            name = name_tag.get_text(strip=True) if name_tag else None
            text_ps = (
                entry.find("div", class_="dipi-flip-box-back-side")
                .find("div", class_="dipi-desc")
                .find_all("p")
            )

            text = "\n".join([text_p.get_text(strip=True) for text_p in text_ps])
            if name and text:
                print(f"Name: {name}")
                print(f"Text: {text}")
                print("-" * 20)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching content for {URL}: {e}")
        return {"name": None, "text": None}


if __name__ == "__main__":
    get_content()
