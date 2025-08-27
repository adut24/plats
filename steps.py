#!/usr/bin/env python3


import os
import requests
from sys import argv
from bs4 import BeautifulSoup
from urllib.parse import urljoin


OUTPUT_DIR = "steps"


def fetch_html(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.text

def extract_text_with_bold(tag) -> str:
    """
    Reconstruit le texte en ajoutant ** autour des morceaux en gras.
    """
    parts = []
    for elem in tag.descendants:
        if elem.name in ["b", "strong"]:
            parts.append(f"**{elem.get_text(strip=True)}**")
        elif elem.name is None:
            text = elem.strip()
            if text:
                parts.append(text)
    return " ".join(parts)

def download_steps(url: str, output_dir: str):
    html = fetch_html(url)
    soup = BeautifulSoup(html, "lxml")

    os.makedirs(output_dir, exist_ok=True)

    steps = soup.find_all("div", {"data-test-id": "instruction-step"})
    print(f"{len(steps)} étapes trouvées.")

    text_lines = []

    for i, step in enumerate(steps, start=1):
        img_tag = step.find("img")
        if img_tag:
            src = img_tag.get("src") or img_tag.get("data-src")
            if src:
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

        instruction_text = extract_text_with_bold(step)
        text_lines.append(f"Étape {i} : {instruction_text}")

    steps_txt = os.path.join(output_dir, "steps.txt")
    with open(steps_txt, "w", encoding="utf-8") as f:
        f.write("\n\n".join(text_lines))

    print(f"\nTexte des étapes sauvegardé dans {steps_txt}")

if __name__ == "__main__":
    download_steps(argv[1], argv[2] + "/" + OUTPUT_DIR)
