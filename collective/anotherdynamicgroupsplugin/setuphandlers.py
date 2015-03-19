# coding=utf8
from .config import PACKAGE_NAME
from .config import PLUGIN_ID
from .plugin import AnotherDynamicGroupsPlugin
from Products.PlonePAS.Extensions.Install import activatePluginInterfaces
from StringIO import StringIO
from plone import api


def import_various(context):
    if context.readDataFile('{}_various.txt'.format(PACKAGE_NAME)) is None:
        return

    portal = context.getSite()
    acl_users = api.portal.get_tool('acl_users')

    if PLUGIN_ID not in acl_users.objectIds():
        plugin = AnotherDynamicGroupsPlugin(
            id=PLUGIN_ID,
            title=PLUGIN_ID.replace('-', ' ').title()
        )
        acl_users._setObject(PLUGIN_ID, plugin)
        activatePluginInterfaces(portal, PLUGIN_ID, StringIO())
