from Products.CMFCore.utils import getToolByName
from Products.PluggableAuthService.plugins.DynamicGroupsPlugin import DynamicGroupDefinition
from zope.app.component.hooks import getSite
from Products.PluggableAuthService.interfaces.plugins import IRolesPlugin

# Here we monkey-patch some methods into `DynamicGroupDefinition` so groups can be displayed by
# the Plone UI.  

DynamicGroupDefinition.getUserName = lambda self: self.id
DynamicGroupDefinition.getName = lambda self: self.id

def getRoles(self):
    portal = getSite()
    acl = getToolByName(portal, 'acl_users')
    rolemakers = acl.plugins.listPlugins(IRolesPlugin)
    
    roles = set()
    
    for (_, rolemaker) in rolemakers:
        roles.update(rolemaker.getRolesForPrincipal(self))    
    
    return list(roles)

DynamicGroupDefinition.getRoles = getRoles