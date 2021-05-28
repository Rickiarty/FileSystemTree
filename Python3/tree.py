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
            if i == len(file_system_objects):
                size += file_system_tree(os.path.join(parent_path, obj), line + '    ', manifest_stream)
            else:
                size += file_system_tree(os.path.join(parent_path, obj), line + '│   ', manifest_stream)
        
        try:
            size += int(os.path.getsize(obj_path))
        except:
            size += int(0)
        i += 1
    
    return size

def construct_tree(start_path, manifest_needed):
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
            manifest_stream = open(os.path.join(os.getcwd(), 'manifest.log'), 'w')
            manifest_stream.write('###\n\nStart path: \n ' + abs_path + '\n')
            manifest_stream.write('.\n')
        total_size = file_system_tree(abs_path, '', manifest_stream)
        print('\nTotal size: ' + format_number_kilo_by_kilo(total_size) + ' byte(s)\n\n###')
        if manifest_needed:
            manifest_stream.write('\nTotal size: ' + format_number_kilo_by_kilo(total_size) + ' byte(s)\n\n###\n')
    except:
        print('\nERROR: The process crashed due to some unknown reason !\n')
        _status_code = -1
    finally:
        if manifest_stream != None:
            manifest_stream.close()
    
    return _status_code

def format_number_kilo_by_kilo(number):
    if number == 0:
        return "0"
    elif number < 0:
        return "-" + format_number_kilo_by_kilo(abs(number))
    
    formatted_str = ""
    count = 0
    while number > 0:
        if count > 0:
            formatted_str = str(number % 1000) + "," + formatted_str
        else:
            formatted_str = str(number % 1000) + formatted_str
        number = number // 1000
        count += 1
    return formatted_str

def main():
    _version_code = '1.1.4' # version code
    manifest_needed = False
    start_path = ''

    if len(sys.argv) == 3:
        if sys.argv[1] == '--manifest':
            manifest_needed = True
            start_path = str(sys.argv[2])
        elif sys.argv[2] == '--manifest':
            manifest_needed = True
            start_path = str(sys.argv[1])
        elif sys.argv[1] == '--version' or sys.argv[2] == '--version':
            print('\n\tversion: ' + _version_code + '\n\t\tby Rei-Chi Lin\n')
            return 1
        else:
            print('\nERROR: Invalid argument(s) !\n')
            return -1
    elif len(sys.argv) == 2:
        if sys.argv[1] == '--version':
            print('\n\tversion: ' + _version_code + '\n\t\tby Rei-Chi Lin\n')
            return 1
        elif sys.argv[1] == '--manifest':
            manifest_needed = True
            start_path = os.getcwd() # get current working directory
        else:
            start_path = str(sys.argv[1])
    elif len(sys.argv) == 1:
        start_path = os.getcwd() # get current working directory
    else:
        print('\nERROR: Too many arguments !\n')
        return -1
    
    _status_code = construct_tree(start_path, manifest_needed)
    return _status_code

if __name__ == '__main__':
    exit_code = main()
    print('\n(exit code: ' + str(exit_code) + ' )')
