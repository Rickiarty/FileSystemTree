#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 * 
 *  Coded by Rei-Chi Lin 
 * 
"""

# The special characters used in this program: 
# "├──Ɖ ",
# "└──Ɖ ",
# "├── ", 
# "└── ", 
# "│   ",
# "    ". 
# (Ɖ: LATIN CAPITAL LETTER AFRICAN D (U+0189) c689)

import os
if __name__ != '__main__':
    from fstree.format_number import format_number_kilo_by_kilo

__version_code = '1.6.4' # version code

def version():
    return __version_code

def file_system_tree(parent_path, line, manifest_stream):
    size = 0
    file_count = 0
    folder_count = 0
    file_system_objects = sorted(os.listdir(parent_path))
    
    i = 1
    for obj in file_system_objects:
        _line = line
        obj_path = os.path.join(parent_path, obj)
        if i == len(file_system_objects):
            if os.path.isdir(obj_path):
                _line += '└──Ɖ ' + obj
            else:
                _line += '└── ' + obj
        else:
            if os.path.isdir(obj_path):
                _line += '├──Ɖ ' + obj
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
            # We have nothing to do in this block. Just skip it.
            # There are no braces '{}' or any symbols other than indents to tell interpreters or compilers how to specify a block of source code in Python. And in Python, once we write a clause such as 'except:', 'finally:', 'else:', ...etc., we cannot leave the block under it blank. And by rules of Python, if we write a clause "try:", we must write at least one corresponding clause 'except:' or 'finally:' for it. 
            # Consequently, we use just a keyword 'pass', which is a null statement in Python, to do nothing but end this block of code.
            pass
        i += 1
    
    return size, folder_count, file_count

__author = 'Rei-Chi Lin'
def author():
    return __author

def construct_tree(start_path, manifest_needed, dir_path_to_save_result):
    _status_code = 0
    abs_path = ''
    try:
        if os.path.exists(start_path) and os.path.isdir(start_path):
            abs_path = os.path.abspath(start_path)
        else:
            print('\nERROR: \n\n The process can not access the given path !\n Please check whether the path exists and whether the path is to a directory/folder.\n And check if the access to the path is permitted or not.\n')
            _status_code = -2
            return _status_code
    except:
        print('\nERROR: \n\n The process can not access the path given !\n Please check whether the path exists.\n And check if the access to the path is permitted or not.\n')
        _status_code = -3
        return _status_code
    
    manifest_stream = None
    try:
        if manifest_needed:
            if os.path.exists(dir_path_to_save_result) and os.path.isdir(dir_path_to_save_result):
                dir_path_to_save_result = os.path.abspath(dir_path_to_save_result)
            else:
                print('\nERROR: \n\n The path to save result cannot be accessed.\n Please check whether the path to save result exists and whether the path is to a directory/folder.\n And check if the access to the path is permitted or not.\n')
                return -5
            manifest_stream = open(os.path.join(dir_path_to_save_result, 'manifest.log'), 'w')
            manifest_stream.write('###\n\nStart path: \n ' + abs_path + '\n')
            manifest_stream.write('.\n')
        print('###\n\nStart path: \n ' + abs_path + '\n')
        print('.')
        total_size, folder_count, file_count = file_system_tree(abs_path, '', manifest_stream)
        if manifest_needed:
            manifest_stream.write('\n' + format_number_kilo_by_kilo(file_count) + ' file(s),\n')
            manifest_stream.write(format_number_kilo_by_kilo(folder_count) + ' folder(s),\n')
            manifest_stream.write('\nTotal size: ' + format_number_kilo_by_kilo(total_size) + ' byte(s)\n\n###\n')
        print('\n' + format_number_kilo_by_kilo(file_count) + ' file(s),')
        print(format_number_kilo_by_kilo(folder_count) + ' folder(s),')
        print('\nTotal size: ' + format_number_kilo_by_kilo(total_size) + ' byte(s)\n\n###')
    except:
        print('\nERROR: The process crashed due to some unknown reason(s) !\n')
        _status_code = -1
    finally:
        if manifest_stream != None:
            manifest_stream.close()
    
    return _status_code

if __name__ == "__main__":
    from format_number import format_number_kilo_by_kilo

    print("ver. " + version() + " by " + author())
    _status_code = construct_tree(os.getcwd(), False, "")
    print('\n(exit code: ' + str(_status_code) + ' )')
    print("\nThe file 'tree.py' is a program unit in module 'fstree', and it should not be used in this way.")
    print("\n---\nAPI usage:\n")
    print("from fstree.tree import construct_tree\n")
    print("status_code = construct_tree(path_to_explore, manifest_needed, dir_path_to_save_result)\n")
    print("path_to_explore :: str")
    print("manifest_needed :: bool")
    print("dir_path_to_save_result :: str")
    print("status_code :: int\n---")
