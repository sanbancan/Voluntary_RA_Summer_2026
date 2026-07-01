import csv
from datetime import datetime, timezone
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

URLS = [
    "https://2-harvest.org/",
    "https://2-harvest.org/get-involved/",
    "https://2-harvest.org/volunteer/",
    "https://2-harvest.org/contact/",
    "https://2-harvest.org/food-rescue/",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
}

def clean_text(text):
    return " ".join(text.split()) if text else ""

def scrape_page(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    title = clean_text(soup.title.get_text()) if soup.title else ""
    meta_desc = ""
    md = soup.find("meta", attrs={"name": "description"})
    if md and md.get("content"):
        meta_desc = clean_text(md["content"])

    headings = []
    for tag in soup.find_all(["h1", "h2", "h3"]):
        t = clean_text(tag.get_text())
        if t:
            headings.append(t)

    links = []
    for a in soup.find_all("a", href=True)[:15]:
        href = urljoin(url, a["href"])
        txt = clean_text(a.get_text())
        if txt or href:
            links.append(f"{txt} -> {href}" if txt else href)

    body_text = clean_text(soup.get_text(" ", strip=True))
    excerpt = body_text[:1200]

    return {
        "scrape_timestamp": datetime.now(timezone.utc).isoformat(),
        "source_url": url,
        "page_title": title,
        "meta_description": meta_desc,
        "headings": " | ".join(headings),
        "top_links": " | ".join(links),
        "body_excerpt": excerpt,
    }

def main():
    rows = []
    for url in URLS:
        try:
            rows.append(scrape_page(url))
        except Exception as e:
            rows.append({
                "scrape_timestamp": datetime.now(timezone.utc).isoformat(),
                "source_url": url,
                "page_title": "",
                "meta_description": "",
                "headings": "",
                "top_links": "",
                "body_excerpt": f"ERROR: {e}",
            })

    out_file = "second_harvest_live_dataset.csv"
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "scrape_timestamp",
                "source_url",
                "page_title",
                "meta_description",
                "headings",
                "top_links",
                "body_excerpt",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {out_file}")

if __name__ == "__main__":
    main()
