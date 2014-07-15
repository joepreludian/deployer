from subprocess import Popen, call, PIPE
import os
from deployer.Utils import CommandExecError, NotConfiguredException, ExecManager, ConfigTemplate
from deployer.controller.Server import Server
import urlparse


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

        logs_folder = '%s/logs' % self.virtual_env
        self._exec(['mkdir', '-p', logs_folder])


    def _pip_install_requirements(self):
        self.append_log('Installing Requirements file...', stdout=True)

        self._exec([self.pip, 'install', '-r', self.requirements_pip])

    def _django_db_setup(self):
        self.append_log('Setting up django database environment...', stdout=True)

        self._exec([self.python, self.manage_py, 'syncdb', '--noinput'])
        self._exec([self.python, self.manage_py, 'migrate'])

    def _django_collectstatic(self):
        self.append_log('Collecting Django static files...')
        self._exec([self.python, self.manage_py, 'collectstatic', '--noinput'])

    def _create_django_superuser(self):
        self.append_log('Adding superuser to rapid login on Django Project...', stdout=True)

        insert_cmd = 'echo "from django.contrib.auth.models import User; ' \
                     'User.objects.create_superuser(\'admin\', \'admin@admin.com\', \'admin\')"' \
                     ' | %s %s shell' % (self.python, self.manage_py)
        call(insert_cmd, stdout=PIPE, stderr=PIPE, shell=True)

    def _get_virtualenv_site_package_dir(self):
        handler = Popen([self.python, '-c',
                         'from distutils.sysconfig import get_python_lib; print get_python_lib()'],
                        stdout=PIPE)
        self.virtualenv_site_packages_dir = handler.communicate()[0]


    def __init__(self, project_name, git_address, site_addr):

        if not project_name or not git_address or not site_addr:
            raise NotConfiguredException('All fields required: Project\'s name, git link and site address')

        Server.__init__(self)

        self.project_name = project_name
        self.git_address = git_address

        self.site_dir = '%s/webapps' % self.home
        self.supervisor_dir = '%s/supervisor' % self.home
        self.nginx_dir = '%s/nginx' % self.home

        self.base_dir = '%s/%s' % (self.site_dir, self.project_name)
        self.supervisor_file = '%s/%s.supervisor.conf' % (self.supervisor_dir, self.project_name)
        self.nginx_file = '%s/%s.nginx.conf' % (self.nginx_dir, self.project_name)

        self.virtual_env = '%s/env' % self.base_dir

        self.site_port = 80
        self.site_url = site_addr

        self.python = '%s/bin/python' % self.virtual_env
        self.pip = '%s/bin/pip' % self.virtual_env

        self.manage_py = '%s/manage.py' % self.base_dir

        self.requirements_pip = '%s/requirements.pip' % self.base_dir
        self.virtualenv_site_packages_dir = '' #will be setted on _get_virtualenv_site_package_dir

        # Nginx Specific stuff
        self.nginx_upstream_resource = "%s_upstream" % self.project_name
        self.gunicorn_socket_file = "%s/sock" % self.virtual_env

        self.log_error_file = "%s/env/logs/nginx-error.log" % self.base_dir
        self.log_access_file = "%s/env/logs/nginx-access.log" % self.base_dir


        self.static_dir = "%s/static/" % self.base_dir  # MUST have ending slash
        self.media_dir = "%s/media/" % self.base_dir


        if self._is_ssh_repo():
            self.git_domain = self.git_address[(self.git_address.find('@')+1):self.git_address.find(':')]
        else:
            self.git_domain = urlparse.urlsplit(self.git_address)[1]

    def _supervisor_install(self):
        self._get_virtualenv_site_package_dir()

        self._exec(['mkdir', '-p', self.supervisor_dir])

        supervisor_file = ConfigTemplate('supervisor_site.conf')
        supervisor_file.render(self)

        supervisor_file.save(self.supervisor_file)

    def _nginx_install_domain(self):

        self._exec(['mkdir', '-p', self.nginx_dir])

        nginx_file = ConfigTemplate('nginx_site.conf')
        nginx_file.render(self)

        nginx_file.save(self.nginx_file)

    def install(self):

        self.append_log('Installing project...', stdout=True)

        self._git_clone()
        self._create_virtualenv()
        self._pip_install_requirements()

        self._django_db_setup()
        self._django_collectstatic()
        self._create_django_superuser()

        self._nginx_install_domain()
        self._supervisor_install()

        return True

    def __getitem__(self, item):
        return getattr(self, item)