#!/usr/bin/env python3
"""Py Shell"""
import sys, cmd, os, subprocess

class ConsoleCode(cmd.Cmd):
    """Our Console code"""

    prompt = '(hbnb) '

    def do_quit(self, arg):
        """Exiting the Console"""

        return True

    def do_EOF(self, arg):
        """Simulating EOF"""

        print(f'{ConsoleCode.prompt}EOF reached')

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

if __name__ == '__main__':
    """Handling interactive and non-interactive mode"""

    if len(sys.argv) > 1:
        command = ' '.join(sys.argv[1:])
        shell = ConsoleCode()
        shell.onecmd(command)
    else:
        try:
            if sys.stdin.isatty():
                ConsoleCode().cmdloop()
            else:
                shell = ConsoleCode()
                print(f'{shell.prompt}')
                for line in sys.stdin:
                    line = line.strip()
                    if line:
                        shell.onecmd(line)
                        print(f'{shell.prompt}')
        except KeyboardInterrupt:
            pass
