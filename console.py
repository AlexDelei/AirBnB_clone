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
from datetime import datetime
from importlib import import_module


class BaseModel:
    """BaseModel Code"""

    def __init__(self, *args, **kwargs):
        """initialising public instances"""

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Saves info into the json file"""

        filename = "file.json"
        try:
            with open(filename, 'r', encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        data[self.id] = self.to_dict()
        with open(filename, 'w', encoding="utf-8") as f:
            json.dump(data, f)

    def to_dict(self):
        """dictionary rep of the instance"""
        return {
                'id': self.id,
                'created_at': self.created_at.isoformat(),
                'updated_at': self.updated_at.isoformat()
                }

    @classmethod
    def load(cls, obj_id):
        """load an instance from json file

        based on class_name and id
        """
        filename = "file.json"
        try:
            with open(filename, 'r') as f_1:
                data = json.load(f_1)
                if isinstance(data, dict):
                    instance_data = data.get(obj_id)
                    if instance_data:
                        instance = cls(**instance_data)
                        return instance
        except json.JSONDecodeError as e:
            print(f"An error occured: {e}")
        return None

    def delete(self):
        """Delete an instance from the file"""

        filename = "file.json"
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                data = [item for item in data if item.get('id') != self.id]

            with open(filename, 'w') as f:
                json.dump(data, f)

        except json.JSONDecodeError as e:
            print(f"An Error occured : {e}")

    @classmethod
    def all(cls):
        """Get a list of string representations

        of all instances"""
        filename = "file.json"""
        instances = []

        try:
            with open(filename, 'r') as f2:
                data = json.load(f2)

                for item in data:
                    inst = cls(**json.loads(item))
                    instances.append(str(inst))
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return instances


class HBNBCommand(cmd.Cmd):
    """Our Console code"""

    prompt = '(hbnb) '

    def do_create(self, arg):
        """creates an instance and saves it to a json file"""

        if not arg:
            print('** class name missing **')
            return

        class_name = arg.split()[0]
        if class_name not in ['BaseModel', 'User']:
            print('** class doesn\'t exist **')
            return
        new_inst = globals()[class_name]()
        new_inst.save()
        print(new_inst.id)

    def do_show(self, arg):
        """prints string representation

        of an instance
        """
        if not arg:
            print('** class name missing **')
            return

        obj_id = arg.split()

        class_name = obj_id[0]

        if class_name not in ['BaseModel', 'User']:
            print('** class doesn\'t exist **')
            return

        if len(obj_id) == 1:
            print('** instance id missing **')
            return

        obj_id = obj_id[1].strip()
        with open("file.json", 'r') as f_4:
            data = json.load(f_4)

            for key in data.keys():
                if '.' in key:
                    class_name, stored_id = key.split('.')
                else:
                    class_name, stored_id = "BaseModel", key

                    if stored_id == obj_id:
                        module = import_module("models.base_model")
                        cls = getattr(module, class_name)
                        obj_instance = cls(**data[key])
                        print(obj_instance)
                        return

            print('** no instance found **')

    def do_destroy(self, arg):
        """Deletes an instance based on

        class name and id"""
        if not arg:
            print("** class name missing **")
            return
        obj_id = arg.split()

        class_name = obj_id[0]

        if class_name not in ['BaseModel', 'User']:
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
                        if class_name not in ['BaseModel', 'User']:
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
        if class_name not in ['BaseModel', 'User']:
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
