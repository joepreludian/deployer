# -*- encoding: utf-8 -*-
import argparse, sys, os
from deployer.controller import Site
from deployer.Utils import CommandExecError
from colorama import Fore


def make_options(subparsers):

    site_parser = subparsers.add_parser('project',
                                     help='Project Help',
                                     )

    site_parser.add_argument('--install',
                          required=False,
                          help='Install help',
                          metavar='',
                          nargs='?',
                          const='install',
                          action=SiteAction)


    site_parser.add_argument('--service',
                          required=False,
                          help='Maintenance help',
                          metavar='MAINTENANCE_OPT',
                          type=str,
                          nargs='?',
                          choices=['maintenance',
                                   'landing',
                                   'block'],
                          action=SiteAction)

    site_parser.add_argument('--update',
                          required=False,
                          help='Update project',
                          metavar='',
                          nargs='?',
                          const='maintenance',
                          action=SiteAction)

    site_parser.add_argument('--uninstall',
                          required=False,
                          nargs='?',
                          help='Uninstall help',
                          const='uninstall',
                          metavar='',
                          action=SiteAction)


    site_parser.add_argument('--name', '-n', help='Project name', required=True)
    site_parser.add_argument('--git', '-g', help='Git Repository')
    site_parser.add_argument('--site-addr', '-s', help='Site Address(es)')
    site_parser.add_argument('--install-to', '-d',
                             metavar='DIR',
                             help='Override install path: default ~/webapps',
                             default='~/webapps')


class SiteAction(argparse.Action):

    def install(self, namespace):

        new_site = Site.Site(project_name=namespace.name,
                             git_address=namespace.git)

        try:
            new_site.install()
        except CommandExecError as error:
            print error
            print "\n%sAppLog%s\n\n%s" % (Fore.RED, Fore.RESET, new_site.output_log())
            sys.exit(1)

        print 'Done!'


    def uninstall(self, namespace):
        print 'Doing uninstall Stuff'
        print namespace

    def maintenance(self, namespace):
        print 'maintenance'
        print namespace

    def landing(self, namespace):
        print 'Landing page'

    def block(self, name):
        print 'Block page'

    def __call__(self, parser, namespace, action, option_string=None):

        try:
            method = getattr(self, action)
        except AttributeError:
            print 'Action not found'
            print action
            sys.exit(2)

        method(namespace)

        sys.exit(0)
