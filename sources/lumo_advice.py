import requests
from bs4 import BeautifulSoup

URL = "https://www.lumoadvice.com/team-sv"


def get_links():
    """
    Fetches a webpage and extracts links to management profiles.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        links = []
        for a_tag in soup.find_all("a", class_="sqs-block-button-element"):
            link = "https://www.lumoadvice.com" + a_tag["href"]
            links.append(link)
        return links
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []


def get_content(link):
    """
    Fetches a management profile page and extracts the name and text.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(link, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        name_tag = soup.find("h2").find("span")
        name = name_tag.get_text(strip=True) if name_tag else None
        text_div = soup.find("section", class_="bright-inverse").find(
            "div", class_="sqs-html-content"
        )
        text = text_div.get_text().strip() if text_div else None
        return {"name": name, "text": text}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content for {link}: {e}")
        return {"name": None, "text": None}


if __name__ == "__main__":
    links = get_links()
    for link in links:
        content = get_content(link)
        if content:
            print(f"Name: {content['name']}")
            print(f"Text: {content['text']}")
        print("-" * 20)
