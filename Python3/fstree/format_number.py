#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 * 
 *  Coded by Rei-Chi Lin 
 * 
"""

from decimal import *

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
    elif int(number) != number:
        return format_number_kilo_by_kilo(int(number)) + str(number - int(number))[1:]
    
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

if __name__ == "__main__":
    num = Decimal(-1002073000.75)
    print(str(num))
    print(format_number_kilo_by_kilo(num))
