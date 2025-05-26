from collective.anotherdynamicgroupsplugin import PLUGIN_ID
from plone import api


def get_plugin():
    pas = api.portal.get_tool("acl_users")
    return pas[PLUGIN_ID]


def add_virtual_group(group_id, title=None):
    plugin = get_plugin()
    plugin.addGroup(group_id=group_id, title=title, predicate="python:False")
