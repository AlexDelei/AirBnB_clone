#!/usr/bin/env python3
"""Py Shell"""
import sys
import cmd
import os
import subprocess
import json
import uuid
from datetime import datetime


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
        try:
            class_name = arg.strip()
            new_inst = globals()[class_name]()
            new_inst.save()
            print(new_inst.id)
        except KeyError:
            print('** class doesn\'t exist **')

    def do_show(self, arg):
        """prints string representation

        of an instance
        """
        args = arg.split()
        if not args:
            print('** class name missing **')
            return

        try:
            class_name, *obj_id = args
            if class_name not in globals():
                print('** class doesn\'t exist **')
                return

            cls = globals()[class_name]
            if not obj_id:
                print('** instance id missing **')
                return

            obj_id = obj_id[0]
            instance = cls.load(obj_id)
            if not instance:
                print('** no instance found **')
                return

            print(instance)
        except ValueError:
            print('** instance id missing **')

    def do_destroy(self, arg):
        """Deletes an instance based on

        class name and id"""
        args = arg.split()
        if not args:
            print('** class name missing **')
            return

        try:
            class_name, *obj_id = args
            if class_name not in globals():
                print('** class doesn\'t exist **')
                return

            cls = globals()[class_name]
            if not obj_id:
                print('** instance id missing **')
                return

            obj_id = obj_id[0]
            instance = cls.load(obj_id)
            if not instance:
                print('** no instance found **')
                return

            instance.delete()
        except ValueError:
            print('** instance id missing **')

    def do_all(self, arg):
        """prints the contents of file.json"""

        filename = "file.json"
        try:
            with open(filename, 'r') as f_t:
                data = json.load(f_t)

                str_rep = []
                for key, value in data.items():
                    if '.' in key:
                        class_name, obj_id = key.split('.')
                    else:
                        class_name, obj_id = "BaseModel", key

                    str_represent = f"[BaseModel] ({obj_id}) {json.dumps(value, default=str)}"
                    str_rep.append(str_represent)

                print(str_rep)
        except FileNotFoundError:
            print("Error File not found")
        except json.JSONDecodeError as e:
            print(f"Error : {e}")

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
        valid_permissions = {'u+x': 0o100, 'u-x': 0o0, 'g+x': 0o010, 'g-x': 0o0}

        if permission not in valid_permissions:
            print('Invalid permission. Use u+x, u-x, g+x, g-x')
            return

        try:
            current_mode = os.stat(file_path).st_mode
            if valid_permissions[permission] & current_mode == 0:
                new_mode = current_mode | valid_permissions[permission]
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
