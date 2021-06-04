#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 * 
 *  Coded by Rei-Chi Lin 
 * 
"""

import os
import sys
from fstree.tree import construct_tree, version

def main():
    manifest_needed = False
    start_path = ''
    dir_path_to_save_result = ''

    if len(sys.argv) == 4:
        if sys.argv[2] == '--manifest':
            manifest_needed = True
            start_path = str(sys.argv[1])
            dir_path_to_save_result = str(sys.argv[3])
        else:
            print("\nERROR: Invalid argument(s) !\n\nType '--help' or '-h' for more info.\n")
            return -6
    elif len(sys.argv) == 3:
        if sys.argv[1] == '--manifest':
            manifest_needed = True
            start_path = os.getcwd() # get current working directory
            dir_path_to_save_result = str(sys.argv[2])
        elif sys.argv[2] == '--manifest':
            manifest_needed = True
            start_path = str(sys.argv[1])
            dir_path_to_save_result = os.getcwd() # get current working directory
        else:
            print("\nERROR: Invalid argument(s) !\n\nType '--help' or '-h' for more info.\n")
            return -6
    elif len(sys.argv) == 2:
        if sys.argv[1] == '--version':
            print('\n\tversion: ' + version() + '\n\t\tby Rei-Chi Lin\n')
            return 2
        elif sys.argv[1] == '--manifest':
            manifest_needed = True
            start_path = os.getcwd() # get current working directory
            dir_path_to_save_result = os.getcwd() # get current working directory
        elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
            help_info = "\nusage:\n\n"
            help_info += "[directory_path_to_explore] [--manifest] [directory_path_to_save_result]\n"
            help_info += "e.g., ~/Downloads --manifest ~/Desktop\n"
            help_info += "\t(to explore under '~/Downloads' and save result under '~/Desktop')\n"
            help_info += "or ~/Downloads --manifest\n"
            help_info += "\t(to explore under '~/Downloads' and save result under current directory)\n"
            help_info += "or --manifest ~/Desktop\n"
            help_info += "\t(to explore under current directory and save result under '~/Desktop')\n"
            help_info += "or --manifest\n"
            help_info += "\t(to explore and save result under current directory)\n"
            help_info += "or ~/Downloads\n"
            help_info += "\t(to explore under '~/Downloads' without saving result)\n"
            help_info += "\nOr just pass no argument to the program.\n"
            help_info += "\t(to explore under current directory without saving result)\n"
            help_info += "\nIf you don't give the program a specific path to explore/save, the default path to explore/save would be your current path.\n"
            print(help_info)
            return 1
        else:
            start_path = str(sys.argv[1])
            dir_path_to_save_result = start_path # (not used)
    elif len(sys.argv) == 1:
        start_path = os.getcwd() # get current working directory
        dir_path_to_save_result = start_path # (not used)
    else:
        print("\nERROR: Too many arguments !\n\nType either '--help' or '-h' for usage info.\n")
        return -4
    
    _status_code = construct_tree(start_path, manifest_needed, dir_path_to_save_result)
    return _status_code

if __name__ == '__main__':
    exit_code = main()
    print('\n(exit code: ' + str(exit_code) + ' )')
