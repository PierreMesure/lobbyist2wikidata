import requests
from bs4 import BeautifulSoup

URL = "https://pauesaberg.se/medarbetare/"


def get_links():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        links = []
        for div in soup.find_all("div", class_="fl-rich-text"):
            a_tag = div.find("a")
            if a_tag:
                links.append(a_tag.get("href"))
        return links
    except requests.exceptions.RequestException as e:
        print(f"Error fetching links: {e}")
        return []


def get_content(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        content_div = soup.find("div", class_="fl-col-small")
        if content_div:
            h1_tag = soup.find("h1")
            if h1_tag:
                for em_tag in h1_tag.find_all("em"):
                    em_tag.extract()
                name = h1_tag.get_text(strip=True)
            else:
                name = None
            if content_div:
                text = content_div.get_text().strip()
            else:
                text = None
            return {"name": name, "text": text}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content for {link}: {e}")
        return None
