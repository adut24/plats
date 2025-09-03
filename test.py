#!/usr/bin/env python3
import json
import os
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import Base, Recette, Categorie, Ingredient, Etape, ingredients_recette

JSON_FILE = "recettes.json"
DB_FILE = "sqlite:///recettes.db"
ASSETS_DIR = "src/"


# --- Fonctions utilitaires ---
def parse_datetime(value):
    if not value:
        return None
    return datetime.fromisoformat(value)


def load_image(path):
    try:
        with open(os.path.join(ASSETS_DIR, path.lstrip("/")), "rb") as f:
            return f.read()
    except Exception:
        return None


def parse_ingredients_file(file_path):
    ingredients = []
    full_path = os.path.join(ASSETS_DIR, file_path.lstrip("/"))
    if not os.path.exists(full_path):
        return ingredients

    with open(full_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            parts = line.strip().split("|")
            if len(parts) < 3:
                continue

            image_path = parts[0].replace("- [IMG]", "").strip()
            quantite = parts[1].strip()
            nom = parts[2].strip()
            allergenes = parts[3].replace("(", "").replace(")", "").strip() if len(parts) > 3 else None

            ingredients.append({
                "image": load_image(image_path),
                "quantite": quantite,
                "nom": nom,
                "allergenes": allergenes
            })

    return ingredients


def parse_steps_file(file_path):
    full_path = os.path.join(ASSETS_DIR, file_path.lstrip("/"))
    steps_texts = {}
    if not os.path.isfile(full_path):
        return steps_texts
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = r"Étape\s+(\d+)\s*:\s*(.*?)(?=(?:Étape\s+\d+\s*:)|\Z)"
    matches = re.findall(pattern, content, flags=re.S)
    for num, text in matches:
        numero = int(num)
        texte = text.strip()
        steps_texts[numero] = texte
    return steps_texts


# --- Insertion ORM ---
def insert_data(session, data):
    for _, r in data.items():
        recette = Recette(
            nom=r["nom"],
            image=load_image(r.get("image_path", "")),
            used=r.get("used"),
            temps_total=r.get("temps_total"),
            created_at=parse_datetime(r.get("created_at")),
            updated_at=parse_datetime(r.get("updated_at"))
        )

        # Catégories
        for cat in r.get("categories", []):
            obj = session.query(Categorie).filter_by(nom=cat).first()
            if not obj:
                obj = Categorie(nom=cat)
            recette.categories.append(obj)

        # Étapes
        steps_texts = {}
        for step in r.get("steps", []):
            if step.endswith(".txt"):
                steps_texts = parse_steps_file(step)

        numero = 1
        for step in r.get("steps", []):
            if step.endswith(".txt"):
                continue
            recette.etapes.append(Etape(
                numero=numero,
                image=load_image(step),
                texte=steps_texts.get(numero)
            ))
            numero += 1

        session.add(recette)
        session.flush()

        for ing in parse_ingredients_file(r.get("ingredients", "")):
            obj = session.query(Ingredient).filter_by(nom=ing["nom"]).first()
            if not obj:
                obj = Ingredient(
                    nom=ing["nom"],
                    image=ing["image"],
                    allergenes=ing["allergenes"]
                )
                session.add(obj)
                session.flush()

            session.execute(
                ingredients_recette.insert().values(
                    id_recette=recette.id,
                    id_ingredient=obj.id,
                    quantite=ing["quantite"]
                )
            )

    session.commit()


def main():
    engine = create_engine(DB_FILE, echo=False, future=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    insert_data(session, data)
    session.close()
    print(f"✅ Migration terminée : {len(data)} recettes importées dans {DB_FILE}")


if __name__ == "__main__":
    main()
