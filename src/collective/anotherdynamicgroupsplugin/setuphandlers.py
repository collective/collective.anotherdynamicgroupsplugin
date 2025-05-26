from collective.anotherdynamicgroupsplugin import PLUGIN_ID
from collective.anotherdynamicgroupsplugin.plugin import AnotherDynamicGroupsPlugin
from io import StringIO
from plone import api
from Products.PlonePAS.setuphandlers import activatePluginInterfaces


def import_various(context):

    portal = context.getSite()
    acl_users = api.portal.get_tool("acl_users")

    if PLUGIN_ID not in acl_users.objectIds():
        plugin = AnotherDynamicGroupsPlugin(
            id=PLUGIN_ID, title=PLUGIN_ID.replace("-", " ").title()
        )
        acl_users._setObject(PLUGIN_ID, plugin)
        activatePluginInterfaces(portal, PLUGIN_ID, StringIO())


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
