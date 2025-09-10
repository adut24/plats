#!/usr/bin/python3
import json
import models
from models.recette import Recette


class FileStorage:
    __file_path = "recettes.json"
    __objects = {}

    def all(self):
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        dict = {}
        for key, value in self.__objects.items():
            dict[key] = value.to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(dict, f)

    def reload(self):
        try:
            with open(self.__file_path, 'r') as f:
                dict = json.load(f)
                for k, v in dict.items():
                    self.__objects[k] = Recette(**v)
        except Exception:
            return


    def delete(self, obj=None) -> None:
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self) -> None:
        self.reload()

    def get(self, id: str) -> Recette | None:
        all_cls = models.storage.all()
        for value in all_cls.values():
            if (value.id == id):
                return value
        return None
