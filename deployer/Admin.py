# -*- encoding: utf8 -*-
import os, sys
from subprocess import call, PIPE
import argparse
from colorama import Fore


def check_app(name):
    return True if call(['which', name],
                        stdout=PIPE,
                        stderr=PIPE) == 0 else False


class StatusAction(argparse.Action):

    def do_checking(self, apps_list):

        for app_tuple in apps_list:
            status = check_app(app_tuple[0])

            print '[ %s%s%s ] %s' % (Fore.GREEN if status else Fore.RED,
                                     'OK' if status else 'FAIL',
                                     Fore.RESET,
                                     app_tuple[1])

    def __call__(self, parser, namespace, values, option_string=None):

        print "Checking services"

        self.do_checking([
            ('node', 'NodeJS'),
            ('gunicorn','Gunicorn'),
            ('mysqld','Mysql Server')
        ])

        sys.exit(0)