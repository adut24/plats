#!/usr/bin/env python3
# pip install requests beautifulsoup4 lxml

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://www.hellofresh.fr/recipes/burger-de-boeuf-au-zaatar-and-aioli-persillee-68597027971405a9ee1f31d0"
OUTPUT_DIR = "steps"

def fetch_html(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.text

def download_step_images(url: str, output_dir: str):
    html = fetch_html(url)
    soup = BeautifulSoup(html, "lxml")

    os.makedirs(output_dir, exist_ok=True)

    steps = soup.find_all("div", {"data-test-id": "instruction-step"})
    print(f"{len(steps)} étapes trouvées.")

    for i, step in enumerate(steps, start=1):
        img_tag = step.find("img")
        if not img_tag:
            continue

        src = img_tag.get("src") or img_tag.get("data-src")
        if not src:
            continue

        img_url = urljoin(url, src)
        filename = os.path.join(output_dir, f"step{i}.jpg")

        try:
            resp = requests.get(img_url, stream=True, timeout=30)
            resp.raise_for_status()
            with open(filename, "wb") as f:
                for chunk in resp.iter_content(1024):
                    f.write(chunk)
            print(f"Téléchargé : {img_url} → {filename}")
        except Exception as e:
            print(f"Erreur pour {img_url} : {e}")

if __name__ == "__main__":
    download_step_images(URL, OUTPUT_DIR)
