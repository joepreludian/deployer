# -*- encoding: utf8 -*-
import argparse, colorama, sys
from deployer.cli import Site, Server, Setup
from deployer.Utils import CommandExecError



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

    try:
        colorama.init()
        print_app_header()

        parser = argparse.ArgumentParser(description='Useful tool to manage webapps projects on VPS')
        subparsers = parser.add_subparsers(help='sub-commands help')

        Setup.make_options(subparsers)
        Server.make_options(subparsers)
        Site.make_options(subparsers)

        parser.parse_args()
    except KeyboardInterrupt:
        print 'Application finished by User.'
        sys.exit(1)
    except OSError, e:
        print "Deployer found an error: %s" % e