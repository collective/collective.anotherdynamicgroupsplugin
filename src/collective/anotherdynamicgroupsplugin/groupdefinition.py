"""Monkey patches to make dynamic groups displayable by the Plone UI.

See: monkey.zcml
"""

from plone import api
from Products.PluggableAuthService.interfaces.plugins import IRolesPlugin


def getUserName(self):
    return self.id


def getName(self):
    return self.id


def getRoles(self):
    acl = api.portal.get_tool("acl_users")
    rolemakers = acl.plugins.listPlugins(IRolesPlugin)

    roles = set()

    for _, rolemaker in rolemakers:
        roles.update(rolemaker.getRolesForPrincipal(self))

    return list(roles)
