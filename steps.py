#!/usr/bin/env python3

import os
import json
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path
from collections import OrderedDict


def fetch_html(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.text


def format_text_with_bold(tag) -> str:
    """Reconstruit un morceau de texte avec ** pour les mots en gras."""
    parts = []
    for elem in tag.descendants:
        if elem.name in ["b", "strong"]:
            parts.append(f"**{elem.get_text(strip=True)}**")
        elif elem.name is None:
            text = elem.strip()
            if text:
                parts.append(text)
    return " ".join(parts)


def parse_recipe_page(url: str, slug: str, assets_dir: Path):
    html = fetch_html(url)
    soup = BeautifulSoup(html, "lxml")

    temps_total = None
    label_span = soup.find("span", {"data-translation-id": "recipe-detail.preparation-time"})
    if label_span:
        parent_span = label_span.find_parent("span")
        if parent_span:
            sibling = parent_span.find_next_sibling("span")
            if sibling:
                temps_total = sibling.get_text(strip=True)

    step_dir = Path("src") / assets_dir / slug / "steps"
    os.makedirs(step_dir, exist_ok=True)

    steps_paths = []
    text_lines = []

    steps = soup.find_all("div", {"data-test-id": "instruction-step"})

    for i, step in enumerate(steps, start=1):
        img_tag = step.find("img")
        if img_tag:
            src = img_tag.get("src") or img_tag.get("data-src")
            if src:
                img_url = urljoin(url, src)
                img_filename = f"step{i}.jpg"
                local_path = step_dir / img_filename
                resp = requests.get(img_url, stream=True, timeout=30)
                resp.raise_for_status()
                with open(local_path, "wb") as f:
                    for chunk in resp.iter_content(1024):
                        f.write(chunk)
                steps_paths.append(f"/{assets_dir.as_posix()}/{slug}/steps/{img_filename}")

        bullets = []
        for sub in step.find_all(["p", "li"]):
            formatted = format_text_with_bold(sub)
            if formatted:
                bullets.append(f"- {formatted}")
        if not bullets:
            fallback_text = format_text_with_bold(step)
            if fallback_text:
                bullets.append(f"- {fallback_text}")
        text_lines.append(f"Étape {i} :\n" + "\n".join(bullets))

    steps_txt_path = step_dir / "steps.txt"
    with open(steps_txt_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(text_lines))

    steps_paths.append(f"/{assets_dir.as_posix()}/{slug}/steps/steps.txt")

    return temps_total, steps_paths


def update_recettes(json_file: Path, url: str, slug: str, assets_dir: Path):
    html = fetch_html(url)
    soup = BeautifulSoup(html, "lxml")

    recipe_name = parse_recipe_name(soup)
    if not recipe_name:
        raise ValueError("Impossible de trouver le titre de la recette dans la page.")

    with open(json_file, "r", encoding="utf-8") as f:
        recettes = json.load(f, object_pairs_hook=OrderedDict)

    key = None
    for k, recette in recettes.items():
        if recette.get("nom") == recipe_name:
            key = k
            break

    if not key:
        raise ValueError(f"Aucune recette trouvée avec le nom '{recipe_name}' dans {json_file}")

    temps_total, steps_paths = parse_recipe_page(url, slug, assets_dir)

    recette = recettes[key]
    new_recette = OrderedDict()
    for k, v in recette.items():
        new_recette[k] = v
        if k == "used":
            new_recette["temps_total"] = temps_total
            new_recette["steps"] = steps_paths

    recettes[key] = new_recette

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(recettes, f, ensure_ascii=True, indent=4)

    print(f"✅ Recette {recipe_name} mise à jour avec temps_total={temps_total} et {len(steps_paths)-1} étapes.")


def parse_recipe_name(soup: BeautifulSoup):
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mise à jour des recettes avec étapes HelloFresh")
    parser.add_argument("--url", required=True, help="URL de la recette HelloFresh")
    parser.add_argument("--slug", required=True, help="Slug utilisé pour le dossier")

    args = parser.parse_args()

    update_recettes(
        json_file=Path("recettes.json"),
        url=args.url,
        slug=args.slug,
        assets_dir=Path("assets/images")
    )
