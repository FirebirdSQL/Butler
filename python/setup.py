#coding:utf-8
"""A setuptools based setup module for FirebirdButlerProtobuf package.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# To use a consistent encoding
from codecs import open
from os import path
# Always prefer setuptools over distutils
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='firebird-butler-protobuf',
    version='0.2.0',
    description='Firebird Butler protocol buffers',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    url='https://github.com/FirebirdSQL/Butler',
    author='Pavel Císař',
    author_email='pcisar@users.sourceforge.net',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',

        'Topic :: Software Development',
        ],
    keywords='Firebird Butler protobuf Saturnin SDK',
    packages=['firebird.butler'],
    zip_safe=False,
    install_requires=['protobuf>=3.9.0'],
    python_requires='>=3.6, <4',
    test_suite='nose.collector',
    data_files=[],
    namespace_packages=[],
    project_urls={
        'Source': 'https://github.com/FirebirdSQL/Butler/python',
        'Documentation': 'https://firebird-butler.readthedocs.io/en/latest/',
        },
    entry_points={}
)
