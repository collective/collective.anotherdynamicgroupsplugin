from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.md").read(),
        open("CONTRIBUTORS.md").read(),
        open("CHANGES.md").read(),
    ]
)

setup(
    name="collective.anotherdynamicgroupsplugin",
    version="1.0.1.dev0",
    description="Another way to define dynamic user groups in Plone.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: 6.1",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="plone pas groups",
    author="Rafael Oliveira",
    author_email="rafaelbco@gmail.com",
    url="http://github.com/collective/collective.anotherdynamicgroupsplugin",
    project_urls={
        "PyPI": "https://pypi.org/project/collective.anotherdynamicgroupsplugin/",
        "Source": "https://github.com/collective/collective.anotherdynamicgroupsplugin",
        "Tracker": "https://github.com/collective/collective.anotherdynamicgroupsplugins",
        "Documentation": "https://github.com/collective/collective.anotherdynamicgroupsplugin",
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["collective"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.9",
    install_requires=[
        "collective.monkeypatcher",
        "setuptools",
        "plone.api",
        "Products.CMFCore",
        "Products.GenericSetup",
        "Products.PlonePAS",
        "Products.PluggableAuthService",
        "zope.component",
        "zope.globalrequest",
        "zope.interface",
        "zope.publisher",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "plone.base",
            "plone.browserlayer",
            "plone.testing>=5.0.0",
            "zest.releaser[recommended]",
            "zestreleaser.towncrier",
            "zope.testrunner",
        ]
    },
    entry_points="""
    [plone.autoinclude.plugin]
    target = plone
    module = collective.anotherdynamicgroupsplugin
    """,
)
