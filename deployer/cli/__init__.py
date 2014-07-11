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

    colorama.init()
    print_app_header()

    # create the top-level parser
    parser = argparse.ArgumentParser(description='Useful tool to manage webapps projects on VPS')
    subparsers = parser.add_subparsers(help='sub-commands help')

    Server.make_options(subparsers)
    Site.make_options(subparsers)

    print_app_header()
    parser.parse_args()