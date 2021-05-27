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
        if os.path.exists(start_path):
            abs_path = os.path.abspath(start_path)
        else:
            print('\nERROR: \n The process can not access the path given !\n Please check whether the path exists.\n And check if the access to the path is permitted or not.\n')
            _status_code = -1
            return _status_code
    except:
        print('\nERROR: \n The process can not access the path given !\n Please check whether the path exists.\n And check if the access to the path is permitted or not.\n')
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
        print('\nTotal size: ' + str(total_size) + ' byte(s)\n\n###')
        if manifest_needed:
            manifest_stream.write('\nTotal size: ' + str(total_size) + ' byte(s)\n\n###\n')
    except:
        print('\nERROR: The process crashed due to some unknown reason !\n')
        _status_code = -1
    finally:
        if manifest_stream != None:
            manifest_stream.close()
    
    return _status_code

def main():
    _version_code = '1.1.0' # version code
    manifest_needed = False
    start_path = ''

    if len(sys.argv) == 3:
        if sys.argv[1] == '--manifest':
            manifest_needed = True
        elif sys.argv[1] == '--version':
            print('\n\tversion: ' + _version_code + '\n\t\tby Rei-Chi Lin\n')
            return 1
        else:
            print('\nERROR: Invalid argument(s) !\n')
            return -1
        start_path = str(sys.argv[2])
    elif len(sys.argv) == 2:
        if sys.argv[1] == '--version':
            print('\n\tversion: ' + _version_code + '\n\t\tby Rei-Chi Lin\n')
            return 1
        else:
            start_path = str(sys.argv[1])
    elif len(sys.argv) == 1:
        start_path = os.getcwd()
    else:
        print('\nERROR: Too many arguments !\n')
        return -1
    
    construct_tree(start_path, manifest_needed)
    return 0

if __name__ == '__main__':
    main()
