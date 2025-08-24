#!/usr/bin/python3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import storage
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/recettes")
def get_recettes():
    return storage.all()

@app.get("/recettes/{id}")
def get_recette(id: str):
    return storage.get(id)

@app.put("/used-true/{id}")
def update_usage_true(id: str):
    recette = storage.get(id)
    if not recette:
        return None
    recette.used = datetime.now()
    recette.save()
    return recette.to_dict()

@app.put("/used-false/{id}")
def update_usage_false(id: str):
    recette = storage.get(id)
    if not recette:
        return None
    recette.used = None
    recette.save()
    return recette.to_dict()
