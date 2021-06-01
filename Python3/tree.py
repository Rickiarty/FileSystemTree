#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 * 
 *  Coded by Rei-Chi Lin 
 * 
"""

# The special characters used in this program: 
# "├── ", 
# "└── ", 
# "│   ". 

import os
import sys

def file_system_tree(parent_path, line, manifest_stream):
    size = 0
    file_count = 0
    folder_count = 0
    file_system_objects = os.listdir(parent_path)
    
    i = 1
    for obj in file_system_objects:
        _line = line
        obj_path = os.path.join(parent_path, obj)
        if i == len(file_system_objects):
            _line += '└── ' + obj
        else:
            _line += '├── ' + obj
        
        print(_line)
        if manifest_stream != None:
            manifest_stream.write(_line + '\n')

        if os.path.isdir(obj_path):
            folder_count += 1
            if i == len(file_system_objects):
                t_size, folder_c, file_c = file_system_tree(os.path.join(parent_path, obj), line + '    ', manifest_stream)
                size += t_size
                folder_count += folder_c
                file_count += file_c
            else:
                t_size, folder_c, file_c = file_system_tree(os.path.join(parent_path, obj), line + '│   ', manifest_stream)
                size += t_size
                folder_count += folder_c
                file_count += file_c
        else:
            file_count += 1
        
        try:
            size += int(os.path.getsize(obj_path))
        except:
            size += int(0)
        i += 1
    
    return size, folder_count, file_count

def construct_tree(start_path, manifest_needed, dir_path_to_save_result):
    _status_code = 0
    abs_path = ''
    try:
        if os.path.exists(start_path) and os.path.isdir(start_path):
            abs_path = os.path.abspath(start_path)
        else:
            print('\nERROR: \n\n The process can not access the given path !\n Please check whether the path exists and whether the path is to a directory/folder.\n And check if the access to the path is permitted or not.\n')
            _status_code = -1
            return _status_code
    except:
        print('\nERROR: \n\n The process can not access the path given !\n Please check whether the path exists.\n And check if the access to the path is permitted or not.\n')
        _status_code = -1
        return _status_code
    
    manifest_stream = None
    try:
        print('###\n\nStart path: \n ' + abs_path + '\n')
        print('.')
        if manifest_needed:
            manifest_stream = open(os.path.join(os.path.abspath(dir_path_to_save_result), 'manifest.log'), 'w')
            manifest_stream.write('###\n\nStart path: \n ' + abs_path + '\n')
            manifest_stream.write('.\n')
        total_size, folder_count, file_count = file_system_tree(abs_path, '', manifest_stream)
        print('\n' + format_number_kilo_by_kilo(file_count) + ' file(s),')
        print(format_number_kilo_by_kilo(folder_count) + ' folder(s),')
        print('\nTotal size: ' + format_number_kilo_by_kilo(total_size) + ' byte(s)\n\n###')
        if manifest_needed:
            manifest_stream.write('\n' + format_number_kilo_by_kilo(file_count) + ' file(s),\n')
            manifest_stream.write(format_number_kilo_by_kilo(folder_count) + ' folder(s),\n')
            manifest_stream.write('\nTotal size: ' + format_number_kilo_by_kilo(total_size) + ' byte(s)\n\n###\n')
    except:
        print('\nERROR: The process crashed due to some unknown reason !\n')
        _status_code = -1
    finally:
        if manifest_stream != None:
            manifest_stream.close()
    
    return _status_code

def padding_number_to_3_digits(number):
    if number < 0:
        return '-' + padding_number_to_3_digits(abs(number))
    numeric_str = ''
    if number == 0:
        numeric_str = '000'
    else:
        if number < 10:
            numeric_str = '00' + str(number)
        else:
            if number < 100:
                numeric_str = '0' + str(number)
            else:
                numeric_str = str(number)
    return numeric_str

def format_number_kilo_by_kilo(number):
    if number == 0:
        return "0"
    elif number < 0:
        return "-" + format_number_kilo_by_kilo(abs(number))
    
    formatted_str = ""
    count = 0
    while number > 0:
        if number // 1000 == 0:
            if count > 0:
                formatted_str = str(number % 1000) + "," + formatted_str
            else:
                formatted_str = str(number % 1000) + formatted_str
        else:
            if count > 0:
                formatted_str = padding_number_to_3_digits(number % 1000) + "," + formatted_str
            else:
                formatted_str = padding_number_to_3_digits(number % 1000) + formatted_str
        number = number // 1000
        count += 1
    return formatted_str

def main():
    _version_code = '1.4.1' # version code
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
            return -1
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
            return -1
    elif len(sys.argv) == 2:
        if sys.argv[1] == '--version':
            print('\n\tversion: ' + _version_code + '\n\t\tby Rei-Chi Lin\n')
            return 1
        elif sys.argv[1] == '--manifest':
            manifest_needed = True
            start_path = os.getcwd() # get current working directory
            dir_path_to_save_result = os.getcwd() # get current working directory
        elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
            help_info = "\nusage:\n\n"
            help_info += "[directory_path_to_search] [--manifest] [directory_path_to_save_result]\n"
            help_info += "e.g., ~/Downloads --manifest ~/Desktop\n"
            help_info += "or ~/Downloads --manifest\n"
            help_info += "or --manifest ~/Desktop\n"
            help_info += "or --manifest\n"
            help_info += "or ~/Downloads\n"
            help_info += "\nOr just pass no argument to the program.\n"
            help_info += "\nIf you didn't give the program a specific path to search, the default path to search would be your current path.\n"
            print(help_info)
            return 1
        else:
            start_path = str(sys.argv[1])
            dir_path_to_save_result = start_path # (not used)
    elif len(sys.argv) == 1:
        start_path = os.getcwd() # get current working directory
        dir_path_to_save_result = start_path # (not used)
    else:
        print("\nERROR: Too many arguments !\n\nType '--help' or '-h' for usage info.\n")
        return -1
    
    _status_code = construct_tree(start_path, manifest_needed, dir_path_to_save_result)
    return _status_code

if __name__ == '__main__':
    exit_code = main()
    print('\n(exit code: ' + str(exit_code) + ' )')
