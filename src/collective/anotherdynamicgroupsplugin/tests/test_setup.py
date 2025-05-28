"""Setup tests for this package."""

from collective.anotherdynamicgroupsplugin.testing import INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.base.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.anotherdynamicgroupsplugin is properly installed."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_product_installed(self):
        """Test if collective.anotherdynamicgroupsplugin is installed."""
        self.assertTrue(
            self.installer.is_product_installed("collective.anotherdynamicgroupsplugin")
        )

    def test_browserlayer(self):
        """Test that IHsmClinicalTrialsLayer is registered."""
        from collective.anotherdynamicgroupsplugin.interfaces import IBrowserLayer
        from plone.browserlayer import utils

        self.assertIn(IBrowserLayer, utils.registered_layers())

    def test_plugin_added(self):
        """Test that IBrowserLayer is removed."""
        from collective.anotherdynamicgroupsplugin import PLUGIN_ID

        self.assertIn(PLUGIN_ID, self.portal.acl_users.objectIds())


class TestUninstall(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        self.installer.uninstall_product("collective.anotherdynamicgroupsplugin")

    def test_product_uninstalled(self):
        """Test if collective.anotherdynamicgroupsplugin is cleanly uninstalled."""
        self.assertFalse(
            self.installer.is_product_installed("collective.anotherdynamicgroupsplugin")
        )

    def test_browserlayer_removed(self):
        """Test that IBrowserLayer is removed."""
        from collective.anotherdynamicgroupsplugin.interfaces import IBrowserLayer
        from plone.browserlayer import utils

        self.assertNotIn(IBrowserLayer, utils.registered_layers())

    def test_plugin_added(self):
        """Test that IBrowserLayer is removed."""
        from collective.anotherdynamicgroupsplugin import PLUGIN_ID

        self.assertNotIn(PLUGIN_ID, self.portal.acl_users.objectIds())
