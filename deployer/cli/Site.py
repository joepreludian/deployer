# -*- encoding: utf-8 -*-
import argparse, sys, os
from deployer.controller import Site
from deployer.Utils import CommandExecError, NotConfiguredException
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

    '''
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
    '''

    site_parser.add_argument('--update',
                          required=False,
                          help='Update project',
                          metavar='',
                          nargs='?',
                          const='update',
                          action=SiteAction)

    site_parser.add_argument('--uninstall',
                          required=False,
                          nargs='?',
                          help='Uninstall help',
                          const='uninstall',
                          metavar='',
                          action=SiteAction)

    site_parser.add_argument('--main-module', '-m', help='Project Main Module', required=True)
    site_parser.add_argument('--name', '-n', help='Project name', required=True)
    site_parser.add_argument('--git', '-g', help='Git Repository')
    site_parser.add_argument('--site-addr', '-s', help='Site Address(es)')


class SiteAction(argparse.Action):

    def install(self, namespace):

        try:
            new_site = Site.Site(project_name=namespace.name,
                                 git_address=namespace.git,
                                 site_addr=namespace.site_addr,
                                 main_module=namespace.main_module)
        except NotConfiguredException, e:
            print 'This tool ins\'t configured. Configure using setup --install'
            print e
            sys.exit(1)

        try:
            new_site.install()
        except CommandExecError as error:
            print error
            print "\n%sAppLog%s\n\n%s" % (Fore.RED, Fore.RESET, new_site.output_log())
            sys.exit(1)

        print 'Done!'

    def uninstall(self, namespace):
        existing_site = Site.Site(project_name=namespace.name)
        existing_site.uninstall()

    def update(self, namespace):
        existing_site = Site.Site(project_name=namespace.name)
        existing_site.update()

    '''
    def maintenance(self, namespace):
        print 'maintenance'
        print namespace

    def landing(self, namespace):
        print 'Landing page'

    def block(self, name):
        print 'Block page'
    '''

    def __call__(self, parser, namespace, action, option_string=None):

        try:
            method = getattr(self, action)
        except AttributeError:
            print 'Action not found'
            print action
            sys.exit(2)

        method(namespace)

        sys.exit(0)
