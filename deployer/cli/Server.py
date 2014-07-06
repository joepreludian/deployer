# -*- encoding: utf8 -*-
import sys, os
from subprocess import call, PIPE
import argparse
from colorama import Fore
from deployer.controller import Server


def make_options(subparsers):

    server_parser = subparsers.add_parser('server', help='a help')
    server_parser.add_argument('--info',
                               type=str,
                               choices=['services',
                                       'environment',
                                       'all'],
                               action=SshAction)
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
