#!/usr/bin/env python3
from models.base_model import BaseModel
from sqlalchemy import Column, Integer, Text, ForeignKey, BLOB
from sqlalchemy.orm import relationship


class Etape(BaseModel):
    id_recette = Column(Integer, ForeignKey("recette.id", ondelete="CASCADE"), nullable=False)
    numero = Column(Integer, nullable=False)
    image = Column(BLOB)
    texte = Column(Text)
    recette = relationship("Recette", back_populates="etapes")
