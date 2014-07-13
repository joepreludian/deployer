import os, sys
from deployer.Utils import ExecManager, NotConfiguredException
from deployer.controller.Setup import DeployerSettings

def get_ssh_pub_key():
    id_rsa_pub_file = '%s/.ssh/id_rsa.pub' % os.environ['HOME']
    try:
        file = open(id_rsa_pub_file, 'r')
    except:
        return False

    return file.read()


class Server(ExecManager):

    def __init__(self):
        ExecManager.__init__(self)

        deployer_settings = DeployerSettings()
        self.config = deployer_settings.get()

        self.home = self.config['home']

        self.known_hosts = '%s/.ssh/known_hosts' % self.base
