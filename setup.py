#coding=utf8
from setuptools import setup, find_packages
import os

version = '0.3'

def read(*paths):
    return open(os.path.join(*paths), 'r').read()

long_description = read('collective', 'anotherdynamicgroupsplugin', 'README.txt')

setup(name='collective.anotherdynamicgroupsplugin',
      version=version,
      description='',
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Rafael Oliveira',
      author_email='rafaelbco@gmail.com',
      url='http://github.com/collective/collective.anotherdynamicgroupsplugin',
      license="''",
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'Plone',
        'z3c.autoinclude',
      ],
      
      extras_require = {
        'test': [
            'plone.app.testing',
        ]
      },
      
      entry_points="""      
      [z3c.autoinclude.plugin]
      target = plone
      """,      
)
