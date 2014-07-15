from distutils.core import setup
from setuptools import find_packages

setup(
    name='deployer',
    version='0.0.3',
    packages=['deployer'],
    package_dir={'deployer': 'deployer'},
    package_data={'mypkg': ['deployer/template/*.conf']},
    url='http://joey.universo42.com.br',
    license='MIT',
    install_requires=['colorama', 'argparse', 'virtualenv'],
    author='Jonhnatha Trigueiro',
    author_email='joepreludian@gmail.com',
    description='A handful tool to install and manage multiple django apps',
    entry_points={
        'console_scripts': [
            'deployer = deployer.cli:main',
        ]
    }
)
