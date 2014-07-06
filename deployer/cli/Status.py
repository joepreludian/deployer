# -*- encoding: utf8 -*-
import sys
import argparse
from colorama import Fore


class StatusAction(argparse.Action):

    def do_checking(self, apps_list):
        response_text = ''
        validated = True

        for app_tuple in apps_list:
            success = check_app(app_tuple[0])

            if not success:
                validated = False

            response_text += '[ %s%s%s ] %s\n' % (Fore.GREEN if success else Fore.RED,
                                                'OK' if success else 'FAIL',
                                                Fore.RESET,
                                                app_tuple[1])
        return validated, response_text

    def __call__(self, parser, namespace, values, option_string=None):

        # Testar se o Development Tools está instalado (groupinstall)

        print "Checking services"
        has_succeed, message = self.do_checking([
            ('node', 'NodeJS'),
            ('npm', 'Npm'),
            ('bower', 'Bower'),
            ('gunicorn','Gunicorn'),
            ('fab','Fabric'),
            ('git','Git command line'),
        ])
        print message

        print 'Checking optional components'
        has_succeed_optionals, message_optionals = self.do_checking([
            ('mysqld','Mysql Server')
        ])
        print message_optionals

        sys.exit(0 if has_succeed else 1)