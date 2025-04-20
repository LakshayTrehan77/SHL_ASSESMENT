import time
import requests
from bs4 import BeautifulSoup
import json
import re

HEADERS = {"User-Agent": "Mozilla/5.0"}
BASE_URL = "https://www.shl.com/solutions/products/product-catalog/"


TYPE_MAP = {
    "K": "Knowledge & Skills",
    "P": "Personality & Behavior",
    "S": "Simulations",
    "A": "Ability & Aptitude",
    "B": "Biodata & Situational Judgement",
    "C": "Competencies",
    "D": "Development",
    "E": "Assessment Exercises"
}

def fetch_paginated_assessment_links(type_param):
    """
    Paginate through the SHL catalog for the given type and collect all assessment URLs.
    Stops when a page returns no new links.
    """
    all_links = set()
    start = 0
    step = 12

    while True:
        url = f"{BASE_URL}?start={start}&type={type_param}&type={type_param}"
        print(f"Fetching: {url}")
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code != 200:
            print(f"Failed to fetch page at start={start}, stopping.")
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        links = {
            (a["href"] if a["href"].startswith("http") else f"https://www.shl.com{a['href']}")
            for a in soup.find_all("a", href=True)
            if "/solutions/products/product-catalog/view/" in a["href"]
        }

        if not links:
            print(f"No more links found at start={start}, stopping.")
            break

        new_links = links - all_links
        if not new_links:
            print(f"No new links found at start={start}, stopping.")
            break

        all_links.update(new_links)
        start += step
        time.sleep(1)

    return list(all_links)


def parse_assessment(url):
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    name_tag = soup.find("h1")
    name = name_tag.get_text(strip=True) if name_tag else "Unknown Assessment"

    desc_div = (soup.find("div", class_="product-description")
                or soup.find("div", class_="product-catalogue-training-calendar__row typ")
                or soup.find("div", class_="rich-text"))

    if desc_div:
        raw_desc = desc_div.get_text(separator=" ", strip=True)
    else:
        raw_desc = " ".join(p.get_text(strip=True) for p in soup.select("main p"))

    description = re.sub(r'^[Dd]escription[\s:–—]*', '', raw_desc)

    remote_icon = soup.select_one("span.ms-2.catalogue__circle.-yes")
    remote = "Yes" if remote_icon else "No"

    adaptive = "No"
    if soup.select_one("span.catalogue__circle.-yes"):
        adaptive = "No"

    
    length = 30  
    length_tag = soup.find("h4", text="Assessment length")
    if length_tag:
        p_tag = length_tag.find_next("p")
        if p_tag:
            length_text = p_tag.get_text(strip=True)
            match = re.search(r"(\d+)", length_text)
            if match:
                length = int(match.group(1))

    
    types = [li.get_text(strip=True) for li in soup.select(".product-types li")]
    if not types:
        if "test" in name.lower(): types.append("A")  
        if "personality" in description.lower(): types.append("P")  
        if not types: types.append("K")  

    test_type_list = [TYPE_MAP.get(t, t) for t in types]  

    return {
        "name": name,
        "url": url,
        "description": description,
        "remote_support": remote,
        "adaptive_support": adaptive,
        "duration": length,
        "test_type": test_type_list
    }


def build_catalog(output_path="catalog.json"):
    
    print("Starting to fetch type=1 assessments...")
    urls_type_1 = fetch_paginated_assessment_links(type_param=1)
    print(f"Found {len(urls_type_1)} type=1 assessment URLs.")
    catalog = []

    for url in urls_type_1:
        try:
            print(f"Parsing: {url}")
            item = parse_assessment(url)
            catalog.append(item)
        except Exception as e:
            print(f"Failed to parse {url}: {e}")

    
    print("\nShifting to fetch type=2 assessments...")
    urls_type_2 = fetch_paginated_assessment_links(type_param=2)
    print(f"Found {len(urls_type_2)} type=2 assessment URLs.")

    for url in urls_type_2:
        try:
            print(f"Parsing: {url}")
            item = parse_assessment(url)
            catalog.append(item)
        except Exception as e:
            print(f"Failed to parse {url}: {e}")

    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
    print(f"Catalog saved to {output_path} with {len(catalog)} items.")


if __name__ == "__main__":
    build_catalog()
