# -*- encoding: utf8 -*-
import sys, os, json
from colorama import Fore
from deployer.Utils import CommandExecError, ExecManager, ConfigTemplate, NotConfiguredException, BASE_DIR

class Installer(ExecManager):

    def __init__(self):
        self.verbose = False

        if not self.is_root():
            raise OSError('You must be have privileges to perform this operation.')

    def _install_pip(self):
        self.append_log('Installing Python packages throught PIP...', stdout=True)
        self._exec(['pip', 'install', 'virtualenv'])
        self._exec(['yum', 'install', 'python-gunicorn', 'supervisor', '-y'])
        self._exec(['yum', 'install', 'supervisor', '-y'])

    def _install_bower(self):
        self.append_log('Installing bower dependencies...', stdout=True)
        self._exec(['npm', '-g', 'install', 'bower'])

    def _install_nodejs(self):
        self.append_log('Installing NodeJS environment...')
        self._exec(['yum', 'install', '-y', 'nodejs', 'npm'])

    def _install_environment_tools(self):
        self.append_log('Installing development tools...', stdout=True)
        self._exec(['yum', 'groupinstall', 'Development Tools', '-y'])
        self._exec(['yum', 'install', 'python-devel', '-y'])

        self.append_log('Installing Nginx...', stdout=True)
        self._exec(['yum', 'install', 'nginx', '-y'])

    def _setup_epel(self):
        self.append_log('Installing repository and Yum stuff...', stdout=True)

        if os.path.isfile('/etc/yum.repos.d/epel.repo'):
            self.append_log('Epel Repo already installed.', stdout=True)
        else:
            self._exec(['yum', 'install', '-y', 'wget'])
            self._exec(['wget', 'http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm',
                        '-O', '/tmp/epel.rpm'])
            self._exec(['rpm', '-ivh', '/tmp/epel.rpm'])
            os.remove('/tmp/epel.rpm')

    def install_requirements(self):
        self.append_log('Installing required software to run deployer. Please Wait...')

        self._setup_epel()
        self._install_environment_tools()

        self._install_pip()

        self._install_nodejs()
        self._install_bower()

        self.append_log('All done!', stdout=True)


class Configurator(ExecManager):

    def __init__(self, supervisor_user, user_home):

        self.verbose = False

        if not supervisor_user or not user_home:
            raise BaseException('username, home folder and/or supervisor supervisor home folder not specified')

        self.config = {'supervisor_user': supervisor_user,
                       'home': user_home}

    def _config_supervisor(self):
        self.append_log('Configuring Supervisor', stdout=True)
        supervisord = ConfigTemplate('supervisord.conf')
        supervisord.render(self.config)
        supervisord.save('/etc/supervisord.conf')

        self.append_log('Enabling supervisord service...')
        self._exec(['chkconfig', 'supervisord', 'on'])


    def _config_nginx(self):
        self.append_log('Configuring Nginx', stdout=True)
        nginx = ConfigTemplate('nginx.conf')
        nginx.render(self.config)
        nginx.save('/etc/nginx/nginx.conf')

        self.append_log('Enabling Nginx service...')
        self._exec(['chkconfig', 'nginx', 'on'])

    def _save_config(self):
        deployer = DeployerSettings()
        deployer.data = self.config
        deployer.save()

    def _setup_ssh_keys(self):
        set_ssh_pub_key()

    def configure(self):
        self.append_log('Configure', stdout=True)
        self._config_supervisor()
        self._config_nginx()
        self._save_config()


class DeployerSettings():

    def __init__(self):
        deployer_config_file = os.path.join(BASE_DIR, 'deployer.conf')

        if not os.path.isfile(deployer_config_file):
            self.data = None
        else:
            with open(deployer_config_file, 'r') as file_handler:
                self.data = json.loads(file_handler.read())

    def get(self):
        if not self.data:
            raise NotConfiguredException()

        return self.data

    def save(self):
        with open(os.path.join(BASE_DIR, 'deployer.conf'), 'w') as file_handler:
            file_handler.write(json.dumps(self.data))
