from setuptools import setup, find_packages

requires = [
    'pika>=1.1.0,<1.2.0'
]

setup(
    name='pika_client',
    version='0.0.1',
    description='Pika client',
    packages=find_packages(),
    install_requires=requires
)
