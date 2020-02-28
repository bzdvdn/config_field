from setuptools import setup, find_packages
from config_field import __version__

setup(
    name='config_field',
    version=__version__,
    packages=find_packages(),
    author='bzdvdn',
    author_email='bzdv.dn@gmail.com',
    url='https://github.com/bzdvdn/config_field',
    install_requires=[
        'Django>=2.2.7',
        'djangorestframework>=3.8.2',
    ]
)
