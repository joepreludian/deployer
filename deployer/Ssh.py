# -*- encoding: utf8 -*-
import sys
from subprocess import call, PIPE
import argparse
from colorama import Fore


def check_app(name):

    return True if call(['which', name],
                        stdout=PIPE,
                        stderr=PIPE) == 0 else False


class SshAction(argparse.Action):

    def __call__(self, parser, namespace, action, option_string=None):

        action = getattr(self, action)
        action()

        sys.exit(0)

    def set(self):
        print 'Make new keys'

    def get(self):
        print 'get existing keys'