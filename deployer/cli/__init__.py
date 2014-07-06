# -*- encoding: utf8 -*-
import argparse
import colorama

from deployer.cli import Site, Server


def print_app_header():
    print '''%s%sPreludian Deployer%s
%sBy Jonhnatha Trigueiro
''' % \
          (colorama.Style.BRIGHT,
           colorama.Fore.GREEN,
           colorama.Fore.RESET,
           colorama.Style.DIM
          )


def main():

    # create the top-level parser
    parser = argparse.ArgumentParser(description='Useful tool to manage webapps projects on VPS')
    subparsers = parser.add_subparsers(help='sub-commands help')

    Server.make_options(subparsers)
    Site.make_options(subparsers)

    print_app_header()
    args = parser.parse_args()

'''
def main():
    colorama.init()

    print header()
    parser = argparse.ArgumentParser()

    parser.add_argument('--status',
                        help='List system requirements if them exists',
                        nargs='?',
                        choices=['all', 'services', 'sites'],
                        action=StatusAction)

    parser.add_argument('--setup',
                        help='Setup environment',
                        nargs='?')

    parser.add_argument('--ssh-keygen',
                        help='Get public keygen',
                        nargs='?',
                        type=str,
                        choices=['set', 'get'],
                        default='get',
                        action=SshAction)

    parser.add_argument('install',
                        nargs='?',
                        help='Installs a new site: install <site_name> <git_repo>')


    parser.parse_args()

    parser.print_help()
'''