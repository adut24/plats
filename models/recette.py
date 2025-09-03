#!/usr/bin/python3
from models.base_model import BaseModel
from sqlalchemy import Column, String, BLOB, TIMESTAMP
from sqlalchemy.orm import relationship
from models import categories_recette, ingredients_recette

class Recette(BaseModel):
    nom = Column(String, nullable=False, index=True)
    image = Column(BLOB)
    used = Column(TIMESTAMP, nullable=True)
    temps_total = Column(String)

    categories = relationship("Categorie", secondary=categories_recette, back_populates="recettes")
    ingredients = relationship("Ingredient", secondary=ingredients_recette, back_populates="recettes")
    etapes = relationship("Etape", back_populates="recette", cascade="all, delete-orphan")
