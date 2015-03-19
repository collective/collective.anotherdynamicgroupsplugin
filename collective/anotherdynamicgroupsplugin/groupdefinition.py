#coding=utf8
from Products.PluggableAuthService.interfaces.plugins import IRolesPlugin
from Products.PluggableAuthService.plugins.DynamicGroupsPlugin import DynamicGroupDefinition
from plone import api

# Here we monkey-patch some methods into `DynamicGroupDefinition` so groups can be displayed by
# the Plone UI.

DynamicGroupDefinition.getUserName = lambda self: self.id
DynamicGroupDefinition.getName = lambda self: self.id


def getRoles(self):
    acl = api.portal.get_tool('acl_users')
    rolemakers = acl.plugins.listPlugins(IRolesPlugin)

    roles = set()

    for (_, rolemaker) in rolemakers:
        roles.update(rolemaker.getRolesForPrincipal(self))

    return list(roles)

DynamicGroupDefinition.getRoles = getRoles
