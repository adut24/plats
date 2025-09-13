#!/usr/bin/python3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import storage
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    now = datetime.now()
    days_ahead = 7 - now.weekday()
    next_monday = datetime(now.year, now.month, now.day) + timedelta(days=days_ahead)
    recette.used = next_monday.replace(hour=0, minute=0, second=0, microsecond=0)
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
