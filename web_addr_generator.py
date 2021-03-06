#!/usr/bin/env python3


import ipaddress
import argparse
import os
from time import sleep


__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20180116'
__version__ = '0.01'
__description__ = ''' Creates a list of URLs to based on an supplied address range,
                      or an input file. Takes the addresses and prepends/appends the
                      appropriate proto/port. '''


http_port_list = ['80', '280', '81', '591', '593', '2080', '2480', '3080', 
                  '4080', '4567', '5080', '5104', '5800', '6080',
                  '7001', '7080', '7777', '8000', '8008', '8042', '8080',
                  '8081', '8082', '8085', '8088', '8089', '8180', '8222', '8280', '8281',
                  '8530', '8887', '9000', '9080', '9090', '16080']                    
https_port_list = ['443', '832', '981', '1311', '1443', '2443', '3443', '4443',
                   '5443', '6443', '7002', '7021', '7023', '7025', '7443',
                   '7777', '8333', '8443', '8531', '8888', '9443', '10443']


def main():
    if args.port:
        for addr in addrs:
            if args.protocol:
                print("{}://{}:{}".format(args.protocol, addr, args.port))
            else:
                print("http://{}:{}".format(addr, args.port))
                print("https://{}:{}".format(addr, args.port))  
                
    elif args.port_filename:
        for addr in addrs:
            for port in port_list:
                if port.endswith('43') or port in https_port_list:
                    print("https://{}:{}".format(addr, port))
                elif port in http_port_list:
                    print("http://{}:{}".format(addr, port))
                else:
                    print("https://{}:{}".format(addr, port))
                    print("http://{}:{}".format(addr, port))
    else:
        for addr in addrs:
            for port in http_port_list:
                print("http://{}:{}".format(addr, port))
            for port in https_port_list:
                print("https://{}:{}".format(addr, port))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--range",
                        help="specify the network range (10.10.10.0/24)")
    parser.add_argument("-f", "--filename",
                        help="specify a file containing the a list of hosts to generate web addresses from.")
    parser.add_argument("-p", "--port",
                        help="specify a file containing the a list of hosts to generate web addresses from.")
    parser.add_argument("-pf", "--port_filename",
                        help="specify a file containing the a list of ports used in place of the default listing.")
    parser.add_argument("-pr", "--protocol",
                        help="specify a protocol to prefix the host. Example -pr https.")
    args = parser.parse_args()

    if not args.filename and not args.range:
        parser.print_help()
        print("\n[-] Please specify an input file (-i) to parse or an IP range (-r)\n")
        exit()
        
    if args.filename and args.range:
        parser.print_help()
        print("\n[-] Please specify an input file (-i) to parse or an IP range (-r)...Not both\n")
        exit()

    if args.filename:
        if not os.path.exists(args.filename):
            parser.print_help()
            print("\n[-] The file cannot be found or you do not have permission to open the file. Please check the path and try again\n")
            exit()
        addrs = open(args.filename).read().splitlines()
        
    if args.port_filename:
        if args.port:
            parser.print_help()
            print("\n[-] Please choose either a port or a port file...Not both\n")
            exit()
        if not os.path.exists(args.port_filename):
            parser.print_help()
            print("\n[-] The file cannot be found or you do not have permission to open the file. Please check the path and try again\n")
            exit()
        port_list = open(args.port_filename).read().splitlines()
        
    if args.port and not args.protocol:
        print("\n[*] No protocol specified. Printing http and https. Use -pr to specifiy protocol.\n")
        sleep(3)

    if args.range:
        addrs = []
        try:
            addr_obj = ipaddress.ip_network(args.range)
        except ValueError:
            parser.print_help()
            print('\n[-] Please do not specify host bits. Example: -r 10.1.1.0/24\n')
            exit()
        for addr in addr_obj.hosts():
            addrs.append(addr)

    main()
