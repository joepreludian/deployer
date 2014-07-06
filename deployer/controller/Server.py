import os, sys


def get_ssh_pub_key():
    id_rsa_pub_file = '%s/.ssh/id_rsa.pub' % os.environ['HOME']
    try:
        file = open(id_rsa_pub_file, 'r')
    except:
        return False

    return file.read()