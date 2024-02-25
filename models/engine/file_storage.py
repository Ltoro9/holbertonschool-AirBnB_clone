#!/usr/bin/python3
"""
    file_storage.py

    Serializes instances to a JSON file and deserializes JSON file to instances
"""


import json


class FileStorage:
    '''
        Serializes and deserializes instances to and from JSON files
    '''
    __file_path = "file.json"
    __objects = {}

    def all(self):
        '''
            Returns all stored objects.
        '''
        return FileStorage.__objects

    def new(self, obj):
        '''
            Adds a new object to the internal dictionary of objects.
        '''
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        '''
            Saves the current state of objects to the JSON file.
        '''
        with open(FileStorage.__file_path, "w") as file:
            new_dict = {k: obj.to_dict()
                        for k, obj in FileStorage.__objects.items()}
            json.dump(new_dict, file)

    def reload(self):
        '''
            Reloads objects from the JSON file
        '''
        from models.base_model import BaseModel
        from models.user import User
        from models.amenity import Amenity
        from models.city import City
        from models.place import Place
        from models.review import Review
        from models.state import State

        try:
            with open(FileStorage.__file_path, "r") as file:
                data = json.load(file)
                for key, value in data.items():
                    class_name = value["__class__"]
                    if class_name == "BaseModel":
                        cls = BaseModel
                    elif class_name == "User":
                        cls = User
                    elif class_name == "Amenity":
                        cls = Amenity
                    elif class_name == "City":
                        cls = City
                    elif class_name == "Place":
                        cls = Place
                    elif class_name == "Review":
                        cls = Review
                    elif class_name == "State":
                        cls = State
                    else:
                        continue
                    obj = cls(**value)
                    FileStorage.__objects[key] = obj
        except FileNotFoundError:
            return
