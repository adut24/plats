#!/usr/bin/env python3
from models.base_model import BaseModel
from sqlalchemy import Column, String, BLOB, Text
from sqlalchemy.orm import relationship
from models.associations import ingredients_recette

class Ingredient(BaseModel):
    nom = Column(String, unique=True, nullable=False, index=True)
    image = Column(BLOB)
    allergenes = Column(Text)
    recettes = relationship("Recette", secondary=ingredients_recette, back_populates="ingredients")
