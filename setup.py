from setuptools import find_packages, setup
import os

# Read the README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='parseify',
    packages=find_packages(include=['parseify']),
    version='0.1',
    description="",
    author='Juan Camilo Lopez',
    install_requires=['requests', 'lxml'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
    long_description=long_description,
    long_description_content_type='text/markdown'

)