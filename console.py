#!/usr/bin/python3
'''
    console.py
    
    Description: Command interpreter entry point
'''
import cmd
import json
import shlex
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    '''
        Command interpreter
    '''
    prompt = '(hbnb) '

    def do_quit(self, arg):
        '''
            Exit program
        '''
        return True

    def do_EOF(self, arg):
        '''
            Exit program with EOF (Ctrl + D)
        '''
        return True

    def cmdloop(self):
        '''
            Handle EOF
        '''
        try:
            with open('file.json', 'r') as file:
                self.objects = json.load(file)
            super().cmdloop()
        except KeyboardInterrupt:
            return True
        finally:
            with open('file.json', 'w') as file:
                json.dump(self.objects, file)

    def emptyline(self):
        '''
            Do nothing (Empty line + Enter)
        '''
        pass

    def do_create(self, arg):
        '''
            Creates a new instance of a class
        '''
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]

        if class_name not in globals():
            print("** class doesn't exist **")
            return

        new_instance = globals()[class_name]()
        new_instance.save()
        print(new_instance.id)

    def all(self):
        '''
            Returns the dictionary representation of all objects
        '''
        objs_dict = {}
        try:
            with open('file.json', 'r') as file:
                objs_dict = json.load(file)
        except FileNotFoundError:
            pass
        return objs_dict

    def do_show(self, arg):
        '''
             Prints the string representation of an instance
        '''
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_id = args[1]
        objs = self.all()
        key = class_name + "." + obj_id
        if key not in objs:
            print("** no instance found **")
            return

        if class_name not in ['User', 'Amenity', 'City', 'Place', 'Review', 'State']:
            print("** class doesn't exist **")
            return

        print(objs[key])  # Print str repr.

    def do_destroy(self, arg):
        '''
                Deletes an instance based on the class name and id
        '''
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_id = args[1]
        objs = self.all()
        key = class_name + "." + obj_id
        if key not in objs:
            print("** no instance found **")
            return

        if class_name not in ['User', 'Amenity', 'City', 'Place', 'Review', 'State']:
            print("** class doesn't exist **")
            return

        del objs[key]
        with open('file.json', 'w') as file:
            json.dump(objs, file)

    def do_all(self, arg):
        '''
            Prints all string representations of User or BaseModel instances
        '''
        if not arg:  # If no arg print all instances
            with open('file.json', 'r') as file:
                objs_dict = json.load(file)
                for key, dictionary in objs_dict.items():
                    class_name, obj_id = key.split('.')
                    if class_name in ['User', 'BaseModel', 'Amenity', 'City', 'Place', 'Review', 'State']:
                        obj_class = globals()[class_name]
                        obj = obj_class(**dictionary)
                        print(obj)
        else:
            args = shlex.split(arg)
            if len(args) == 1:
                class_name = args[0]
                if class_name in ['User', 'BaseModel', 'Amenity', 'City', 'Place', 'Review', 'State']:
                    with open('file.json', 'r') as file:
                        data = json.load(file)
                        for key, value in data.items():
                            if value["__class__"] == class_name:
                                obj_repr = f"[{class_name}] ({key.split('.')[1]}) {value}"
                                print(obj_repr)

                else:
                    print("** class doesn't exist **")

    def do_update(self, arg):
        '''
            Update instance based on the class name and id
        '''
        args = shlex.split(arg)
        args = args[:4]  # Only first 4 arguments are used

        if len(args) == 0:
            print('** class name missing **')
            return
        class_name = args[0]

        if class_name not in ['User', 'BaseModel', 'Amenity', 'City', 'Place', 'Review', 'State']:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print('** instance id missing **')
            return
        obj_id = args[1]

        try:

            with open("file.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            print("** no instance found **")
            return
        key = f"{class_name}.{obj_id}"

        if key not in data:
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return
        attr_name = args[2]

        if len(args) < 4:
            print('** value missing **')
            return

        attr_value = " ".join(args[3:])  # Handle attr value with spaces
        obj_dict = data[key]
        obj_dict[attr_name] = attr_value  # Update attr

        with open("file.json", "w") as file:
            json.dump(data, file)

        # Construct the str repr
        obj_repr = f"[{class_name}] ({obj_id}) {obj_dict}"

        with open("updated_instances.txt", "a") as file:
            file.write(obj_repr + "\n")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
