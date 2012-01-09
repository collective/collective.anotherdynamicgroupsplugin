#coding=utf8
from ..testing import INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing.interfaces import (TEST_USER_ID, TEST_USER_PASSWORD, TEST_USER_ROLES, 
    TEST_USER_NAME)
import unittest2 as unittest
from ..util import add_virtual_group

class PloneTestCase(unittest.TestCase):
    """Tests if we play nice with Plone."""
    
    layer = INTEGRATION_TESTING    
    
    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        
    def test_should_not_break_usergroup_groupprefs(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        
        add_virtual_group('group1')
        
        html = self._render_view('usergroup-groupprefs')
        
        f = open('/tmp/a.html', 'w')
        f.write(html)
        f.close()
    
    def _render_view(self, view):
        view_url = self.portal.absolute_url() + '/@@' + view
        self.request.set('URL', view_url)
        self.request.set('ACTUAL_URL', view_url)        
        
        return self.portal.unrestrictedTraverse('@@' + view)()        
