# -*- encoding: utf8 -*-
import argparse, sys
import colorama
import Admin


def main():
    colorama.init()

    parser = argparse.ArgumentParser()

    parser.add_argument('--status',
                        help='List system requirements if them exists',
                        nargs='?',
                        choices=['all', 'services', 'sites'],
                        default='all',
                        action=Admin.StatusAction)

    parser.add_argument('--setup',
                        help='Setup environment',
                        nargs='?')

    parser.add_argument('--ssh-keygen',
                        help='Get public keygen',
                        nargs='?',
                        type=str)

    parser.add_argument('install',
                        nargs='?',
                        help='Installs a new site: install <site_name> <git_repo>')


    parser.parse_args()

    #print colorama.Fore.RED + 'Preludian Deployer' + colorama.Fore.RESET
    #parser.print_help()