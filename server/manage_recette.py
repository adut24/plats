#!/usr/bin/env python3
import os
import json
import requests
from sys import argv
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path
from collections import OrderedDict
from models.recette import Recette
from datetime import datetime
import uuid
import shlex
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unicodedata
from PIL import Image
import io
import difflib


def fetch_html(url: str) -> str:
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.text


def format_text_with_bold(tag) -> str:
    parts = []
    for elem in tag.descendants:
        if elem.name in ['b', 'strong']:
            parts.append(f'**{elem.get_text(strip=True)}**')
        elif elem.name is None:
            text = elem.strip()
            if text:
                parts.append(text)
    return ' '.join(parts)


def parse_recipe_page(url: str, slug: str, assets_dir: Path):
    html = fetch_html(url)
    soup = BeautifulSoup(html, 'lxml')

    temps_total = None
    label_span = soup.find('span', {'data-translation-id': 'recipe-detail.preparation-time'})
    if label_span:
        parent_span = label_span.find_parent('span')
        if parent_span:
            sibling = parent_span.find_next_sibling('span')
            if sibling:
                temps_total = sibling.get_text(strip=True)

    step_dir = Path('..') / Path('client') / Path('src') / assets_dir / slug / 'steps'
    os.makedirs(step_dir, exist_ok=True)

    steps_paths = []
    text_lines = []

    steps = soup.find_all('div', {'data-test-id': 'instruction-step'})

    for i, step in enumerate(steps, start=1):
        img_tag = step.find('img')
        if img_tag:
            src = img_tag.get('src') or img_tag.get('data-src')
            if src:
                img_url = urljoin(url, src)
                img_filename = f'step{i}.jpg'
                local_path = step_dir / img_filename
                resp = requests.get(img_url, stream=True, timeout=30)
                resp.raise_for_status()
                with open(local_path, 'wb') as f:
                    for chunk in resp.iter_content(1024):
                        f.write(chunk)
                steps_paths.append(f'/{assets_dir.as_posix()}/{slug}/steps/{img_filename}')

        bullets = []
        for sub in step.find_all(['p', 'li']):
            formatted = format_text_with_bold(sub)
            if formatted:
                bullets.append(f'- {formatted}')
        if not bullets:
            fallback_text = format_text_with_bold(step)
            if fallback_text:
                bullets.append(f'- {fallback_text}')
        text_lines.append(f'Étape {i} :\n' + '\n'.join(bullets))

    steps_txt_path = step_dir / 'steps.txt'
    with open(steps_txt_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(text_lines))

    steps_paths.append(f'/{assets_dir.as_posix()}/{slug}/steps/steps.txt')

    return temps_total, steps_paths


def update_recettes(json_file: Path, url: str, slug: str, assets_dir: Path) -> None:
    html = fetch_html(url)
    soup = BeautifulSoup(html, 'lxml')

    recipe_name = parse_recipe_name(soup)
    if not recipe_name:
        raise ValueError('Impossible de trouver le titre de la recette dans la page.')

    with open(json_file, 'r', encoding='utf-8') as f:
        recettes = json.load(f, object_pairs_hook=OrderedDict)

    key = None
    for k, recette in recettes.items():
        if recette.get('nom') == recipe_name:
            key = k
            break

    if not key:
        noms_existants = [r.get("nom") for r in recettes.values()]
        similaires = difflib.get_close_matches(recipe_name, noms_existants, n=5, cutoff=0.6)

        if similaires:
            print(f"Aucune recette exactement nommée '{recipe_name}' trouvée.")
            print("⚠️ Recettes au nom similaire :")
            for i, nom in enumerate(similaires, start=1):
                print(f"[{i}] {nom}")
            print("[0] Aucune de ces recettes")
            choix = input("Choisir une recette à mettre à jour (numéro) ou 0 pour ajouter : ").strip()

            if choix.isdigit() and int(choix) > 0 and int(choix) <= len(similaires):
                nom_choisi = similaires[int(choix) - 1]
                for k, recette in recettes.items():
                    if recette.get("nom") == nom_choisi:
                        key = k
                        break
            else:
                raise ValueError(f"Aucune recette sélectionnée, '{recipe_name}' sera proposée à l’ajout.")
        else:
            raise ValueError(f"Aucune recette trouvée avec le nom '{recipe_name}' dans {json_file}.")

    temps_total, steps_paths = parse_recipe_page(url, slug, assets_dir)
    ingredients_path = parse_ingredients(url, slug, assets_dir)

    recette = recettes[key]
    new_recette = OrderedDict()
    for k, v in recette.items():
        new_recette[k] = v
        if k == 'used':
            new_recette['temps_total'] = temps_total
            new_recette['steps'] = steps_paths
            new_recette['ingredients'] = ingredients_path

    recettes[key] = new_recette

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(recettes, f, indent=4)

    print(f'✅ Recette {recipe_name} mise à jour.')


def parse_recipe_name(soup: BeautifulSoup) -> str | None:
    h1 = soup.find('h1')
    if h1:
        return h1.get_text(strip=True)
    return None

def check_ajout_recette() -> str:
    choix: str = ''
    while choix not in ['1', '2']:
        print('Ajouter la recette ?')
        print('[1] Oui')
        print('[2] Non')
        choix = input('choix : ')
    return choix


def add_recette(url: str, slug: str, assets_dir: Path = Path('assets/images')):
    html = fetch_html(url)
    soup = BeautifulSoup(html, 'lxml')

    recipe_name = parse_recipe_name(soup)
    if not recipe_name:
        raise ValueError('Impossible de trouver le titre de la recette dans la page.')
    dir = Path('..') / Path('client') / Path('src') / assets_dir / slug
    step_dir = dir / 'steps'
    os.makedirs(step_dir, exist_ok=True)
    plat = soup.find('img', {'alt': recipe_name})
    image_path = None
    if plat:
        src = plat.get('src') or plat.get('data-src')
        if src:
            img_url = urljoin(url, src)
            img_filename = f'plat.jpg'
            image_path = dir / img_filename
            resp = requests.get(img_url, stream=True, timeout=30)
            resp.raise_for_status()
            with open(image_path, 'wb') as f:
                for chunk in resp.iter_content(1024):
                    f.write(chunk)
    attributs = dict()
    attributs.update({"id": str(uuid.uuid4())})
    attributs.update({"nom": recipe_name})
    attributs.update({"categories": shlex.split(input("categories : "))})
    attributs.update({"image_path": image_path.as_posix().removeprefix('src') if image_path else None})
    attributs.update({"used": None})
    temps_total, steps_paths = parse_recipe_page(url, slug, assets_dir)
    ingredients_path = parse_ingredients(url, slug,  assets_dir)
    attributs.update({"temps_total": temps_total})
    attributs.update({"steps": steps_paths})
    attributs.update({"ingredients": ingredients_path})
    now = datetime.now().isoformat()
    attributs.update({"created_at": now})
    attributs.update({"updated_at": now})
    recette = Recette(**attributs)
    recette.new()
    print(f'✅ Recette {recipe_name} ajoutée avec temps_total={temps_total} et {len(steps_paths)-1} étapes.')


def clean_ingredient_name(name: str) -> str:
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("utf-8")
    name = name.lower().strip()
    stopwords = {"de", "du", "des", "d", "en", "au", "aux", "la", "le", "les", "et"}
    tokens = [t for t in re.split(r"\W+", name) if t and t not in stopwords]
    return "_".join(tokens)

def parse_ingredients(url: str, slug: str, assets_dir: Path):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    wait = WebDriverWait(driver, 10)
    btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-pseudocontent="2"]'))
    )
    btn.click()
    time.sleep(2)

    ing_dir = Path('..') / Path('client') / Path("src") / assets_dir / slug
    os.makedirs(ing_dir, exist_ok=True)
    ingredients_txt_path = ing_dir / "ingredients.txt"

    global_ing_dir = Path("../client/src/assets/images/ingredients")
    os.makedirs(global_ing_dir, exist_ok=True)

    ingredients = []
    divs = driver.find_elements(
        By.CSS_SELECTOR, 'div[data-test-id="ingredient-item-shipped"], div[data-test-id="ingredient-item-not-shipped"]'
    )

    for div in divs:
        parts = []
        text_divs = div.find_elements(By.TAG_NAME, "div")
        if len(text_divs) >= 2:
            p_tags = text_divs[1].find_elements(By.TAG_NAME, "p")
            lines = [p.text.strip() for p in p_tags if p.text.strip()]

            quantity = lines[0] if len(lines) > 0 else ""
            ingredient_name = lines[1] if len(lines) > 1 else ""
            allergen = lines[2] if len(lines) > 2 else ""

            clean_name = clean_ingredient_name(ingredient_name)

            try:
                img = div.find_element(By.TAG_NAME, "img")
                if img:
                    img_src = img.get_attribute("src") or img.get_attribute("data-src")
                    if img_src:
                        filename = f"{clean_name}.png"
                        filepath = global_ing_dir / filename

                        if not filepath.exists():
                            resp = requests.get(img_src, stream=True, timeout=30)
                            resp.raise_for_status()
                            img_obj = Image.open(io.BytesIO(resp.content)).convert("RGBA")
                            img_obj.save(filepath, format="PNG")

                        parts.append(f"[IMG] /assets/images/ingredients/{filename}")
            except Exception:
                pass

            segments = []
            if quantity.strip():
                segments.append(quantity.strip())
            if ingredient_name.strip():
                segments.append(ingredient_name.strip())
            if allergen.strip():
                segments.append(allergen.strip())

            full_text = " | ".join(segments)
            full_text = re.sub(r"(\d)([A-Za-zÀ-ÖØ-öø-ÿ])", r"\1 \2", full_text)

            if full_text:
                parts.append(full_text)

        if parts:
            ingredients.append("- " + " | ".join(parts))

    driver.quit()

    if ingredients:
        with open(ingredients_txt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(ingredients))
        return f"/{assets_dir.as_posix()}/{slug}/ingredients.txt"
    return None

if __name__ == '__main__':
    try:
        update_recettes(
            json_file=Path('recettes.json'),
            url=argv[1],
            slug=argv[2],
            assets_dir=Path('assets/images')
        )
    except ValueError as e:
        print(e)
        choix = check_ajout_recette()
        if choix == '1':
            add_recette(url=argv[1], slug=argv[2])
