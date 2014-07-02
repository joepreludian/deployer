# -*- encoding: utf8 -*-
import os
from subprocess import call, PIPE
import argparse
from colorama import Fore


def check_app(name):
    return True if call(['which', name],
                        stdout=PIPE,
                        stderr=PIPE) == 0 else False


class StatusAction(argparse.Action):

    def check_app_result(self, appname, message):
        status = check_app(appname)

        return '[ %s%s%s ] %s' % (Fore.GREEN if status else Fore.RED,
                                 'OK' if status else 'FAIL',
                                 Fore.RESET,
                                 message)

    def __call__(self, parser, namespace, values, option_string=None):

        print self.check_app_result('node',
                                    'Checking presence of NodeJS')
        print self.check_app_result('ls',
                                    'Checking presence of LS')

