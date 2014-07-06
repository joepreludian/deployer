from subprocess import Popen, call, PIPE
import os
from deployer.Utils import CommandExecError
import urlparse


def get_project_dir(project_name):
    return '%s/webapps/%s' % (os.environ['HOME'], project_name)


def get_project_git_domain(git):

    if git.find('@') != -1:
        is_ssh_repo = True
        return is_ssh_repo, git[(git.find('@')+1):git.find(':')]
    else:
        is_ssh_repo = False
        url_splitted = urlparse.urlsplit(git)
        return is_ssh_repo, url_splitted[1]

def update_ssh_known_keys(raw_git_ssh_key):
    known_hosts_file = '%s/.ssh/known_hosts' % os.environ['HOME']

    file_handler = open(known_hosts_file, 'r') if os.path.isfile(known_hosts_file) else None
    data_check = file_handler.read() if file_handler else ''

    if data_check.find(raw_git_ssh_key.strip()) == -1:
        if file_handler:
            file_handler.close()

        file_handler = open(known_hosts_file, 'w')
        file_handler.write(raw_git_ssh_key)

    file_handler.close()


def register_ssh_git_domain(git):
    is_ssh_repo, repository_domain = get_project_git_domain(git)

    if is_ssh_repo:
        p = Popen(['ssh-keyscan', '-H', repository_domain], stdout=PIPE, stderr=PIPE)
        ssh_key_fetch_from_domain = p.stdout.read()

        update_ssh_known_keys(ssh_key_fetch_from_domain)


def git_clone(project_name, git):

    project_dir = get_project_dir(project_name=project_name)
    call(['mkdir', '-p', project_dir])

    register_ssh_git_domain(git)

    error_code = call(['git', 'clone', git, project_dir])

    if error_code == 128:
        raise CommandExecError('It Seems You dont Have a valid git repo. May Be wrong keys or repo may exists on destiny path.')

    return True

def install(project_name, git):
    return git_clone(project_name, git)
