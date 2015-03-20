#coding=utf8
from setuptools import setup
from setuptools import find_packages
import os

version = '1.0.1.dev0'


def read(*paths):
    return open(os.path.join(*paths), 'r').read()

long_description = read('README.txt') + '\n\n' + read('docs', 'HISTORY.txt')

setup(
    name='collective.anotherdynamicgroupsplugin',
    version=version,
    description='Another way to define dynamic user groups in Plone.',
    long_description=long_description,
    # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='plone pas groups',
    author='Rafael Oliveira',
    author_email='rafaelbco@gmail.com',
    url='http://github.com/collective/collective.anotherdynamicgroupsplugin',
    license='GPL version 2',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Plone',
        'z3c.autoinclude',
        'plone.api',
        'collective.monkeypatcher',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
    test_suite='tests',
)
