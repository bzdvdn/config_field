from setuptools import setup, find_packages

setup(
    name='config_field',
    version='0.4.5',
    packages=find_packages(),
    author='bzdvdn',
    author_email='bzdv.dn@gmail.com',
    url='https://github.com/bzdvdn/config_field',
    setup_requires=[
        'Django>=2.2.7',
        'djangorestframework>=3.8.2',
    ],
)
