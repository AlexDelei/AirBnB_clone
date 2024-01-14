#!/usr/bin/env python3
"""Py Shell"""
import sys
import cmd
import os
import subprocess
import json
import uuid
import ast
import shlex
import models
from models.base_model import BaseModel
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User
from models.state import State
from models.city import City
from datetime import datetime
from importlib import import_module


class HBNBCommand(cmd.Cmd):
    """Our Console code"""

    prompt = '(hbnb) '

    classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

    def do_create(self, arg):
        """creates an instance and saves it to a json file"""

        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in self.classes:
            instance = self.classes[args[0]]()
        else:
            print("** class doesn't exist **")
            return False
        print(instance.id)
        instance.save()

    def do_show(self, arg):
        """prints string representation

        of an instance
        """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in self.classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Deletes an instance based on

        class name and id"""
        if not arg:
            print("** class name missing **")
            return
        obj_id = arg.split()

        class_name = obj_id[0]

        if class_name not in self.classes:
            print('** class doesn\'t exist **')
            return

        if len(obj_id) == 1:
            print('** instance id missing **')
            return
        obj_id = obj_id[1].strip()
        try:
            with open("file.json", 'r') as f_5:
                data = json.load(f_5)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        instance_found = False
        for key in data.keys():
            if '.' in key:
                class_name, stored_id = key.split('.')
            else:
                class_name, stored_id = "BaseModel", key

                if stored_id == obj_id:
                    del data[key]
                    instance_found = True
                    break
        with open("file.json", 'w') as f_6:
            json.dump(data, f_6)

        if not instance_found:
            print(f'** no instance found **')

    def do_all(self, arg):
        """prints the contents of file.json"""

        filename = "file.json"
        try:
            with open(filename, 'r') as f_t:
                data = json.load(f_t)

                class_name = None
                if arg:
                    class_name = arg.strip()
                    try:
                        if class_name not in self.classes:
                            raise NameError
                    except NameError:
                        print('** class doesn\'t exist **')
                        return

                str_rep = []
                for key, value in data.items():
                    if '.' in key:
                        class_name, obj_id = key.split('.')
                    else:
                        class_name, obj_id = "BaseModel", key

                    str_rpr = (
                            f"[BaseModel] ({obj_id}) "
                            f"{json.dumps(value, default=str)}"
                            )
                    str_rep.append(str_rpr)

                print(str_rep)
        except FileNotFoundError:
            print("Error File not found")
        except json.JSONDecodeError as e:
            print(f"Error : {e}")

    def do_update(self, arg):
        """updates an instance based on class nae and id"""

        args = shlex.split(arg)

        if len(args) < 1:
            print('** class name missing **')
            return
        class_name = args[0]
        if not class_name:
            print('** class name missing **')
            return
        if class_name not in self.classes:
            print('** class doesn\'t exist **')
            return

        if len(args) < 2:
            print('** instance id missing **')
            return
        obj_id = args[1]

        filename = "file.json"
        try:
            with open(filename, 'r') as f_7:
                data = json.load(f_7)
        except FileNotFoundError:
            data = {}

        instance_key = f'{obj_id}'
        if instance_key not in data:
            print('** no instance found **')
            return
        if len(args) < 3:
            print('** attribute name missing **')
            return
        attr_name = args[2]
        if len(args) < 4:
            print('** value missing **')
            return
        attr_val = args[3]
        instance_data = data[instance_key]
        if 'first_name' in instance_data:
            instance_data['first_name'] = attr_val

        with open(filename, 'w') as f_8:
            json.dump(data, f_8)

    def do_quit(self, arg):
        """Quit command to exit the program

        """
        return True

    def do_EOF(self, arg):
        """Simulating EOF"""

        return True

    def do_mkdir(self, arg):
        """creates new directory"""

        try:
            os.mkdir(arg)
        except FileExistsError:
            print(f'Directory {arg} already exists')

    def do_cd(self, arg):
        """Changes into new directory"""

        try:
            os.chdir(arg)
        except FileNotFoundError:
            print(f'Directory {arg} not found')
        except PermissionError:
            print(f'Permission denied to access {arg}')

    def do_vi(self, arg):
        """implemeting the vi text editor"""

        subprocess.run(['vi', arg])

    def do_ls(self, arg):
        """Lists all files,directories in the current dir and the specified"""

        if not arg:
            arg = '.'
        try:
            files = os.listdir(arg)
            for i in files:
                file_path = os.path.join(arg, i)
                if os.path.isdir(file_path):
                    print('\033[94m' + i + '\033[0m')
                elif os.access(file_path, os.X_OK):
                    print('\033[92m' + i + '\033[0m')
                else:
                    print(i)
        except FileNotFoundError:
            print(f'Directory not found: {arg}')
        except PermissionError:
            print(f'Permission denied to access {arg}')

    def do_clear(self, arg):
        """clears the screen"""

        os.system('clear' if os.name == 'posix' else 'cls')

    def do_chmod(self, arg):
        """Chnages the mode of a file"""

        args = arg.split()
        if len(args) != 2:
            print('Usage: chmod <permission> <file>')
            return
        permission, file_path = args
        valid_permission = {'u+x': 0o100, 'u-x': 0o0, 'g+x': 0o010, 'g-x': 0o0}

        if permission not in valid_permission:
            print('Invalid permission. Use u+x, u-x, g+x, g-x')
            return

        try:
            current_mode = os.stat(file_path).st_mode
            if valid_permission[permission] & current_mode == 0:
                new_mode = current_mode | valid_permission[permission]
                os.chmod(file_path, new_mode)
        except FileNotFoundError:
            print(f'File not found: {file_path}')
        except PermissionError:
            print("Permission denied")

    def emptyline(self):
        """Do nothing if its empty line"""

        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
