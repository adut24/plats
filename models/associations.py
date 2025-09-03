#!/usr/bin/env python3
from sqlalchemy import Table, Column, ForeignKey, String, Index
from models.base_model import Base


categories_recette = Table(
    "categories_recette",
    Base.metadata,
    Column("id_recette", ForeignKey("recette.id", ondelete="CASCADE"), primary_key=True),
    Column("id_categorie", ForeignKey("categorie.id", ondelete="CASCADE"), primary_key=True),
)

ingredients_recette = Table(
    "ingredients_recette",
    Base.metadata,
    Column("id_recette", ForeignKey("recette.id", ondelete="CASCADE"), primary_key=True),
    Column("id_ingredient", ForeignKey("ingredient.id", ondelete="CASCADE"), primary_key=True),
    Column("quantite", String)
)

Index("idx_categories_recette", categories_recette.c.id_recette, categories_recette.c.id_categorie)

Index("idx_ingredients_recette", ingredients_recette.c.id_recette, ingredients_recette.c.id_ingredient)
