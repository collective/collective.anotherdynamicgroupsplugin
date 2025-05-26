from collective.anotherdynamicgroupsplugin import PLUGIN_ID
from collective.anotherdynamicgroupsplugin.plugin import AnotherDynamicGroupsPlugin
from io import StringIO
from plone import api
from Products.PlonePAS.setuphandlers import activatePluginInterfaces


def post_install(context):

    portal = api.portal.get()
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

    acl_users = api.portal.get_tool("acl_users")
    plugins = acl_users.objectIds()
    if PLUGIN_ID in plugins:
        acl_users.manage_delObjects([PLUGIN_ID])

