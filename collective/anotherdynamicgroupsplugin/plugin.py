from .interfaces import IGroupProvider
from Products.CMFCore.utils import getToolByName
from Products.PlonePAS.interfaces.group import IGroupIntrospection
from Products.PlonePAS.tools.groupdata import GroupData
from Products.PluggableAuthService.plugins.DynamicGroupsPlugin import DynamicGroupsPlugin
from Products.PluggableAuthService.utils import classImplements
from zope.component import getAdapters
from zope.globalrequest import getRequest
    
class AnotherDynamicGroupsPlugin(DynamicGroupsPlugin):
    
    def getGroupsForPrincipal(self, principal, request=None):        
        """Override `DynamicGroupsPlugin`."""
        if request is None:
            request = getRequest()
                
        groups = set()
        providers = [a for (_, a) in getAdapters((principal, request), IGroupProvider)]

        for p in providers:
            groups.update(p())
        
        return list(groups)
                    
    def getGroupById(self, group_id):
        """Implementation of `IGroupIntrospection`."""
        if group_id not in self.listGroupIds():
            return None
            
        gtool = getToolByName(self, 'portal_groupdata')
        group = self[group_id]
                
        return gtool.wrapGroup(group)
        
    def getGroups(self):
        """Implementation of `IGroupIntrospection`."""
        return [self.getGroupById(id) for id in self.listGroupIds()]    
   
    def getGroupIds(self):
        """Implementation of `IGroupIntrospection`."""
        return self.listGroupIds()
    
    def getGroupMembers(self, group_id):
        """Implementation of `IGroupIntrospection`."""
        return []        
    
classImplements(AnotherDynamicGroupsPlugin, IGroupIntrospection)    