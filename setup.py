from setuptools import setup
from setuptools import find_packages


VERSION = '1.0.0'

setup(
    name='getusee',
    version=VERSION,
    description='Make selenium more easy, but chrome only!',
    packages=find_packages(),
    zip_safe=False,
)