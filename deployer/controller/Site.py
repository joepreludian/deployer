from subprocess import Popen, call, PIPE
import os
from deployer.Utils import CommandExecError
import urlparse


class Server():

    def __init__(self):
        self.base = os.environ['HOME']
        self.known_hosts = '%s/.ssh/known_hosts' % self.base


class Site(Server):

    def _is_ssh_repo(self):
        return True if self.git_address.find('@') != -1 else False

    def _update_server_ssh_key(self):
        if self._is_ssh_repo():
            p = Popen(['ssh-keyscan', '-H', self.git_domain], stdout=PIPE, stderr=PIPE)
            ssh_key_fetch_from_domain = p.stdout.read()

            file_handler = open(self.known_hosts, 'r') if os.path.isfile(self.known_hosts) else None
            data_check = file_handler.read() if file_handler else ''

            if data_check.find(ssh_key_fetch_from_domain.strip()) == -1:
                if file_handler:
                    file_handler.close()

                file_handler = open(self.known_hosts, 'w')
                file_handler.write(ssh_key_fetch_from_domain)

            file_handler.close()

    def _git_clone(self):

        self._update_server_ssh_key()

        call(['mkdir', '-p', self.base_dir])
        error_code = call(['git', 'clone', self.git_address, self.base_dir])

        if error_code == 128:
            raise CommandExecError('It Seems You dont Have a valid git repo. May Be wrong keys or repo may exists on destiny path.')

        return True

    def _create_virtualenv(self):
        return call(['virtualenv', self.virtual_env])

    def _pip_install_requirements(self):
        return call([self.pip, 'install', '-r', self.requirements_pip])

    def _django_db_setup(self):
        call([self.python, self.manage_py, 'syncdb', '--noinput'])
        call([self.python, self.manage_py, 'migrate'])

    def __init__(self, project_name, git_address):

        Server.__init__(self)

        self.project_name = project_name
        self.git_address = git_address

        self.base_dir = '%s/webapps/%s' % (os.environ['HOME'], self.project_name)
        self.virtual_env = '%s/env' % (self.base_dir)

        self.python = '%s/bin/python' % (self.virtual_env)
        self.pip = '%s/bin/pip' % (self.virtual_env)

        self.manage_py = '%s/manage.py' % (self.base_dir)

        self.requirements_pip = '%s/requirements.pip' % self.base_dir

        if self._is_ssh_repo():
            self.git_domain = self.git_address[(self.git_address.find('@')+1):self.git_address.find(':')]
        else:
            self.git_domain = urlparse.urlsplit(self.git_address)[1]

    def install(self):
        self._git_clone()
        self._create_virtualenv()
        self._pip_install_requirements()

        self._django_db_setup()

        return True