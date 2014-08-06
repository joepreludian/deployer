import os, sys
from subprocess import call
from deployer.Utils import ExecManager, NotConfiguredException, CommandExecError
from deployer.controller.Setup import DeployerSettings

def get_ssh_pub_key():
    id_rsa_pub_file = '%s/.ssh/id_rsa.pub' % os.environ['HOME']
    try:
        file = open(id_rsa_pub_file, 'r')
    except:
        return False

    return file.read()

def set_ssh_pub_key():
    call(['ssh-keygen', '-t', 'rsa'])


class Server(ExecManager):

    def __init__(self):
        ExecManager.__init__(self)

        deployer_settings = DeployerSettings()

        try:
            self.config = deployer_settings.get()
        except OSError:
            raise NotConfiguredException()

        self.home = self.config['home']
        self.user = self.config['supervisor_user']

        self.known_hosts = '%s/.ssh/known_hosts' % self.home

    def services_reload(self):
        try:
            self._exec(['sudo', 'service', 'nginx', 'reload'])
        except CommandExecError:
            self._exec(['sudo', 'service', 'nginx', 'start'])

        self.append_log('Reloaded Nginx over sudo.', stdout=True)

        try:
            self._exec(['sudo', 'service', 'supervisord', 'reload'])
        except CommandExecError:
            self._exec(['sudo', 'service', 'supervisord', 'start'])

        self.append_log('Reloaded Supervisord over sudo.', stdout=True)

    def services_restart(self):
        try:
            self._exec(['sudo', 'service', 'nginx', 'restart'])
        except CommandExecError:
            self._exec(['sudo', 'service', 'nginx', 'start'])

        self.append_log('Restarted Nginx over sudo.', stdout=True)

        try:
            self._exec(['sudo', 'service', 'supervisord', 'restart'])
        except CommandExecError:
            self._exec(['sudo', 'service', 'supervisord', 'start'])

        self.append_log('Restarted Supervisord over sudo.', stdout=True)