#!/usr/bin/env python3
from models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.associations import categories_recette

class Categorie(BaseModel):
    nom = Column(String, unique=True, nullable=False, index=True)
    recettes = relationship("Recette", secondary=categories_recette, back_populates="categories")
