# -*- encoding: utf8 -*-
import sys, os
import argparse
from colorama import Fore
from deployer.controller import Setup, Info
from deployer import Utils


def make_options(subparsers):

    server_parser = subparsers.add_parser('setup', help='Usefull for setup server')
    server_parser.add_argument('--install',
                               type=str,
                               choices=['requirements',
                                       'config',
                                       'all'],
                               action=SetupAction,
                               required=True)
    server_parser.add_argument('--supervisor-user', '-u',
                               type=str,
                               help='User used by supervisor to manage their sites')
    server_parser.add_argument('--deployer-home', '-c',
                               type=str,
                               help='Folder used by Deployer to manage per site config. ~/ would be nice.')

class SetupAction(argparse.Action):

    def __call__(self, parser, namespace, action, option_string=None):

        try:
            action = getattr(self, action)
        except AttributeError:
            print 'Action not found'

        action(namespace)

        sys.exit(0)

    def requirements(self):
        setup = Setup.Installer()
        setup.verbose = True

        try:
            setup.install_requirements()
        except Utils.CommandExecError, e:
            print 'Deployer found an error. Will be describled below:'
            print e
            print setup.output_log()

    def config(self, namespace):
        try:
            configurator = Setup.Configurator(supervisor_user=namespace.supervisor_user,
                                              user_home=namespace.deployer_home)
        except BaseException:
            print 'You must set --supervisor-name, --deployer-home before --install'
            sys.exit(1)

        configurator.configure()

    def all(self, namespace):
        self.requirements()
        self.config(namespace)