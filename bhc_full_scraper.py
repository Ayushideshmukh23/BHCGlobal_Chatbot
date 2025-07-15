import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

base_url = "https://bhcglobal.com"
visited = set()
site_data = {}

def scrape_page(url):
    print(f"Scraping: {url}")
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')

        texts = [p.get_text(strip=True) for p in soup.find_all('p')]
        headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])]

        site_data[url] = {
            "headings": headings,
            "paragraphs": texts
        }

        links = set()
        for a in soup.find_all('a', href=True):
            href = a['href']
            full_url = urljoin(base_url, href)
            if urlparse(full_url).netloc == urlparse(base_url).netloc and full_url.startswith(base_url):
                links.add(full_url)

        return links

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return set()

to_visit = set([base_url])

while to_visit:
    current_url = to_visit.pop()
    if current_url not in visited:
        visited.add(current_url)
        new_links = scrape_page(current_url)
        to_visit.update(new_links - visited)
        time.sleep(1)

with open("bhc_site_data.txt", "w", encoding='utf-8') as f:
    for page, content in site_data.items():
        f.write(f"\nURL: {page}\n")
        f.write("Headings:\n" + "\n".join(content["headings"]) + "\n")
        f.write("Paragraphs:\n" + "\n".join(content["paragraphs"]) + "\n")
        f.write("\n" + "="*60 + "\n")

print("✅ Done! Content saved to bhc_site_data.txt")
