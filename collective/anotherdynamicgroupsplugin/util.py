from zope.app.component.hooks import getSite
from .config import PLUGIN_ID
from Products.CMFCore.utils import getToolByName

def get_plugin():
    portal = getSite()
    pas = getToolByName(portal, 'acl_users')
    return pas[PLUGIN_ID]

def add_virtual_group(group_id, title=None):
    plugin = get_plugin()
    plugin.addGroup(group_id=group_id, title=title, predicate='python:False')
