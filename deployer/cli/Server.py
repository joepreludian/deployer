# -*- encoding: utf8 -*-
import sys, os
from subprocess import call, PIPE
import argparse
from colorama import Fore
from deployer.controller import Server
from deployer.controller.Info import check_if_present


def make_options(subparsers):

    server_parser = subparsers.add_parser('server', help='a help')
    server_parser.add_argument('--info',
                               type=str,
                               choices=['services',
                                       'environment',
                                       'all'],
                               action=InfoAction)

    server_parser.add_argument('--ssh',
                               type=str,
                               choices=['get',
                                        'set'],
                               action=SshAction)


class SshAction(argparse.Action):

    def __call__(self, parser, namespace, action, option_string=None):

        try:
            action = getattr(self, action)
        except AttributeError:
            print 'Action not found'

        action()

        sys.exit(0)

    def set(self):
        call(['ssh-keygen', '-t', 'rsa'])

    def get(self):
        ssh_pubkey = Server.get_ssh_pub_key()
        if ssh_pubkey:
            print ssh_pubkey
        else:
            print "Pubkey not generated. Try to create one!"


class InfoAction(argparse.Action):

    def do_checking(self, apps_list):

        response_text = ''
        has_success_all, return_data = check_if_present(apps_list)

        for item in return_data:

            response_text += '[ %s%s%s ] %s\n' % (Fore.GREEN if item[1] else Fore.RED,
                                                'OK' if item[1] else 'FAIL',
                                                Fore.RESET,
                                                item[0].capitalize())

        return has_success_all, response_text

    def __call__(self, parser, namespace, values, option_string=None):

        # Testar se o Development Tools está instalado (groupinstall)

        print "Checking services\n"

        has_succeed_all, services_print = self.do_checking(['node',
                                                            'git',
                                                            'npm',
                                                            'bower',
                                                            'gunicorn',
                                                            'fab',
                                                            'supervisord'])

        print services_print

        if not has_succeed_all:
            print '%sIt seems you do not have all require software to run properly this server.%s' % \
                  (Fore.RED, Fore.RESET)

        sys.exit(0 if has_succeed_all else 1)