#!/usr/bin/python3
from datetime import datetime
import models
import uuid


Base = object
time = '%Y-%m-%dT%H:%M:%S.%f'


class Recette:
    id: str
    nom: str
    used: datetime
    categories: list
    image_path: str
    created_at: datetime
    updated_at: datetime


    def __init__(self, *args, **kwargs):
        if kwargs:
            for k, v in kwargs.items():
                if k in ["created_at", "updated_at"]:
                    setattr(self, k, datetime.strptime(v, time))
                elif k == "used" and v is not None:
                    setattr(self, k, datetime.strptime(v, time))
                else:
                    setattr(self, k, v)
        else:
            self.id = str(uuid.uuid4())
            self.nom = str(args[0]).replace('"', '')
            self.image_path = str(args[1]).replace('"', '')
            self.categories = [str(s).replace('"', '') for s in args[2:]]
            self.used = None
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        new_dict = self.__dict__.copy()
        new_dict.update({"created_at": self.created_at.isoformat()})
        new_dict.update({"updated_at": self.updated_at.isoformat()})
        if self.used is not None:
            new_dict.update({"used": self.used.isoformat()})
        new_dict.update({"categories": self.categories})
        new_dict.update({"image_path": self.image_path})
        return new_dict

    def delete(self):
        models.storage.delete(self)
