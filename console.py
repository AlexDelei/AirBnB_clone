#!/usr/bin/env python3
"""Py Shell"""
import sys
import cmd
import os
import subprocess


class HBNBCommand(cmd.Cmd):
    """Our Console code"""

    prompt = '(hbnb) '

    def do_quit(self, arg):
        """Quit command to exit the program"""

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
