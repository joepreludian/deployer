# -*- encoding: utf8 -*-
import sys, os
from subprocess import call, PIPE
import argparse
from colorama import Fore


def check_app(name):

    return True if call(['which', name],
                        stdout=PIPE,
                        stderr=PIPE) == 0 else False


class SshAction(argparse.Action):

    def __call__(self, parser, namespace, action, option_string=None):

        try:
            action = getattr(self, action)
            action()
        except TypeError:
            print 'Action not found'

        sys.exit(0)

    def set(self):
        call(['ssh-keygen', '-t', 'rsa'])

    def get(self):
        id_rsa_pub_file = '%s/.ssh/id_rsa.pub' % os.environ['HOME']
        success = call(['cat', id_rsa_pub_file], stderr=PIPE)

        if success != 0:
            print "It seems you don't have a SSH Key. Try to create one!"
