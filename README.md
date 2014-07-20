##Preludian Deployer

A Smart command line tool for deploy/maintain small Django applications easily throught in VPS instances.
This Tool is in ALPHA. Some commands should be replaced. Please do not use this on production. (Yet)

###What this tool can offer to you

The tool purpose is to install Django (at first moment) applications on simple VPS by providing small informations. The tool also installs what they need to run properly in setup.

###Requirements

er was designed to run on Fedora20. After I will improve to other platforms. To install this alpha you should use PIP. If Your VPS do not have PIP, please install throught:

    # yum install python-pip 

###Setup

To install this use the following command, as root:

    # pip install git+https://github.com/joepreludian/deployer
Once installed you must setup the Deployer basic config. It recommended You create a standard user to setup this. In the example below I create a user called olympus. Look how the command would be:

    # deployer setup --supervisor-user olympus --deployer-home /home/olympus --install all
This command will install all needed packages to get deployer running. It will configure Nginx and Supervisord to be running at startup. Also will create a sudoers file to give permissions to the following user ONLY to restart services.

    $ deployer server --ssh set
This command will create a brand new SSH. It the same as ssh-keygen -t rsa. You MUST run this command with the user you setted up the system.

Usage

To setup a new Django project, do:

    $ deployer project --name todolist --git https://github.com/joepreludian/todo-list --site-addr "todo.universo42.com.br" --install

This is the main goal of this tool. You must set a project name (--name), a git repo (--git) and a Site(s) Address(es) (--site-addr) that the site must be configured to bind to.

The Django project must have:

* requirements.pip file
* Django South Installed

This command will create on deployer's home folder (--deployer-home) the following folders:
* webapps -> Containing the application itself. One project per folder.
* nginx -> Have the nginx config files
* supervisor -> Have the supervisor.conf files for each project

###Questions?

Please feel free to help me sharing experiences, opening issues, setting up stuffs, doing Documentation or giving me a couple of coffee! =D