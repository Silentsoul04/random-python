#!/usr/bin/env python3

__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20180514'
__version__ = '0.01'
__description__ = """A program to plot byte values for a given set of data"""


import matplotlib.pyplot as plt 
import base64
import urllib.parse
import argparse
import os
import time


def decode_url_encoding(input_string):
    """Returns a URL decoded byte-string
    """
    if type(input_string) == bytes:
        input_string = input_string.decode()
    if '%' not in input_string:
        return input_string.encode()
    return urllib.parse.unquote(input_string).encode()


def get_integer_list(input_bytes):
    """Returns a list of byte integers from a byte-string.
    """
    return [byte for byte in input_bytes]


def create_byte_histogram(input_bytes):
    """Returns a dictionary containing each byte value as a key and the
    number of times it occures in the input bytes as a value.
    """
    bytes_dict = dict()
    for byte in input_bytes:
        bytes_dict[byte] = bytes_dict.get(byte, 0) + 1
    return bytes_dict

    
def check_byte_representation(bytes_dict):
    """Generates a list of all possible 256 bytes values and returns any
    byte value that does not appear as a key in the supplied dictionary.
    """
    missing_byte_list = []
    total_bytes = [byte for byte in range(256)]
    for byte in total_bytes:
        if byte not in bytes_dict:
            missing_byte_list.append(byte)
    return missing_byte_list
        

def plot_histogram(data):
    """Plots a histogram from the given data.
    """
    plt.hist(data, color='g')
    plt.title('Byte Histogram')
    plt.ylabel('Occurence')
    plt.xlabel('Byte Values')
    plt.xticks(range(0, 256, 10))
    plt.show()


def plot_scatter(data):
    """Plots a scatter chart from the given data.
    """
    positions = [i for i in range(len(data))]
    plt.scatter(data_list, positions, edgecolors='r')
    plt.title('Byte Scatter Plot')
    plt.ylabel('Occurence')
    plt.xlabel('Byte Values')
    plt.xticks(range(0, 256, 10))
    plt.show()


def main():
    data = input_data
    if type(data) == str:
        data = data.encode()
    if args.url_decode:
        data = decode_url_encoding(data)
    if args.b64_decode:
        data = base64.b64decode(data)
    data_list = get_integer_list(data)
    integer_list = [i for i in range(256)]
    if args.plot_histogram:
        plot_histogram(data_list)
    if args.plot_scatter:
        plot_scatter(data_list)
    print("[*] Processing {}...".format(data[:50]))
    time.sleep(1)
    data_dict = create_byte_histogram(data)
    print("[*] Checking if all bytes are represented")
    time.sleep(1)
    missing_bytes = check_byte_representation(data_dict)
    missing_byte_count = sum([1 for byte in missing_bytes])
    print("[+] {} bytes positions are not represented in the data".format(missing_byte_count))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",
                        help="Increase output verbosity", 
                        action="store_true")
    parser.add_argument("-ph", "--plot_histogram",
                        help="Plot at histogram.", 
                        action="store_true")
    parser.add_argument("-ps", "--plot_scatter",
                        help="Plot as scatter.", 
                        action="store_true")
    parser.add_argument("-d", "--data",
                        help="Specify the data as a string.")
    parser.add_argument("-f", "--file",
                        help="Specify a file containing the data.")
    parser.add_argument("-u", "--url_decode",
                        help="Decode the URL encoded characters", 
                        action="store_true")
    parser.add_argument("-b", "--b64_decode",
                        help="Decode the b64 encoded data", 
                        action="store_true")
    args = parser.parse_args()

    if not args.data and not args.file:
        parser.print_help()
        print('\n[-] Please specify the encrypted data (-d data) or specify a file containing the data (-f /path/to/data) ')
        exit()
    if args.data and args.file:
        parser.print_help()
        print('\n[-] Please specify either -d or -f, not both.')
        exit()
    if args.data:
        input_data = args.data
    if args.file:
        if not os.path.exists(args.file):
            print("\n[-] The file cannot be found or you do not have permission to open the file. Please check the path and try again\n")
            exit()
        else:
            with open(args.file, 'rb') as fh:
                input_data = fh.read()
    main()
