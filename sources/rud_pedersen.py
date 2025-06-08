import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.rudpedersen.com/sv/kontakt"


def get_links():
    """
    Fetches a webpage, extracts links, and retrieves JSON data.
    """
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, "html.parser")

        script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
        json_data = {}
        if script_tag:
            try:
                json_data = json.loads(script_tag.string)
            except json.JSONDecodeError:
                print("Error decoding JSON data.")

        data = json_data["props"]["pageProps"]["stories"]["contactPersons"]
        links = [
            "https://www.rudpedersen.com/"
            + item["full_slug"].replace("rud-pedersen", "")
            for item in data
        ]
        return links

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []


def get_content(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        name_div = soup.select_one("h1[class^=PageContactPerson_title]")
        name = name_div.get_text(strip=True) if name_div else None

        text_div = soup.select_one("div[class*=PageContactPerson_text]")
        text = text_div.get_text(strip=True) if text_div else None

        return {"name": name, "text": text}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content for {link}: {e}")
        return None


if __name__ == "__main__":
    links = get_links()
    for link in links:
        content = get_content(link)
        if content:
            print(f"Name: {content['name']}")
            print(f"Text: {content['text']}")
        print("-" * 20)
