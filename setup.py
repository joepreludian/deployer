from distutils.core import setup
from setuptools import find_packages

setup(
    name='deployer',
    version='0.0.1',
    packages=find_packages(),
    url='http://joey.universo42.com.br',
    license='MIT',
    requires=['colorama', 'virtualenv'],
    author='Jonhnatha Trigueiro',
    author_email='joepreludian@gmail.com',
    description='A handful tool to manage multiple django apps',
    entry_points={
        'console_scripts': [
            'deployer = deployer.cli:main',
        ]
    }
)
