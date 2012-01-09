"""Set-up dos doctests."""
import unittest2 as unittest
import doctest
from plone.testing import layered
from ..testing import INTEGRATION_TESTING
import collective.anotherdynamicgroupsplugin

def _globalize_layer_resources(test, resources):
    for k in resources:
        test.globs[k] = test.globs['layer'][k]

def _setUp(test):
    global BASEDIR
    _globalize_layer_resources(test, ['portal', 'request'])
        
def _tearDown(test):
    pass
    
_globs = {} 

_options = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE

def _create_docfile_suite(filename, package):
    return layered(
        doctest.DocFileSuite(
            filename, 
            module_relative=True, 
            package=package,
            globs=_globs,
            setUp=_setUp,
            tearDown=_tearDown,
            optionflags=_options,
        ),
        layer=INTEGRATION_TESTING
    )

def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        _create_docfile_suite('README.txt', package=collective.anotherdynamicgroupsplugin),
    ])
    return suite
