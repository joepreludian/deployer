from subprocess import Popen, call, PIPE
import os
from deployer.Utils import CommandExecError, ExecManager, ConfigTemplate
import urlparse


class Server(ExecManager):

    def __init__(self):
        ExecManager.__init__(self)

        self.base = os.environ['HOME']
        self.known_hosts = '%s/.ssh/known_hosts' % self.base


class Site(Server):

    def _is_ssh_repo(self):
        return True if self.git_address.find('@') != -1 else False

    def _update_server_ssh_key(self):

        self.append_log('Checking SSH Keys database...', stdout=True)

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
        self.append_log('Cloning Repo...', stdout=True)

        self._update_server_ssh_key()

        self._exec(['mkdir', '-p', self.base_dir])
        self._exec(['git', 'clone', self.git_address, self.base_dir])


    def _create_virtualenv(self):
        self.append_log('Creating Virtualenv...', stdout=True)

        self._exec(['virtualenv', self.virtual_env])

    def _pip_install_requirements(self):
        self.append_log('Installing Requirements file...', stdout=True)

        self._exec([self.pip, 'install', '-r', self.requirements_pip])

    def _django_db_setup(self):
        self.append_log('Setting up django database environment...', stdout=True)

        self._exec([self.python, self.manage_py, 'syncdb', '--noinput'])
        self._exec([self.python, self.manage_py, 'migrate'])

    def _create_django_superuser(self):
        self.append_log('Adding superuser to rapid login on Django Project...', stdout=True)

        insert_cmd = 'echo "from django.contrib.auth.models import User; ' \
                     'User.objects.create_superuser(\'admin\', \'admin@admin.com\', \'admin\')"' \
                     ' | %s %s shell' % (self.python, self.manage_py)
        call(insert_cmd, stdout=PIPE, stderr=PIPE, shell=True)

    def _nginx_install_domain(self):
        config_file = ConfigTemplate('nginx.conf')

        config_file.render(self)

        print config_file

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

        # Nginx Specific stuff
        self.nginx_upstream_resource = "%s_upstream" % self.project_name
        self.gunicorn_socket_file = "%s/sock" % self.virtual_env

        self.log_error_file = "%s/env/logs/nginx-error.log" % self.base_dir
        self.log_access_file = "%s/env/logs/nginx-access.log" % self.base_dir


        self.site_port = 80
        self.site_url = 'http://teste.com.br'

        self.static_dir = "%s/static/" % self.base_dir  # MUST have ending slash
        self.media_dir = "%s/media/" % self.base_dir


        if self._is_ssh_repo():
            self.git_domain = self.git_address[(self.git_address.find('@')+1):self.git_address.find(':')]
        else:
            self.git_domain = urlparse.urlsplit(self.git_address)[1]


    def install(self):

        self.append_log('Installing project...', stdout=True)

        '''
        self._git_clone()
        self._create_virtualenv()
        self._pip_install_requirements()

        self._django_db_setup()
        self._create_django_superuser()
        '''
        self._nginx_install_domain()

        return True

    def __getitem__(self, item):
        return getattr(self, item)