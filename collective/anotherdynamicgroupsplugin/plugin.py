from Products.PluggableAuthService.plugins.DynamicGroupsPlugin import DynamicGroupsPlugin
from zope.globalrequest import getRequest
from zope.component import getAdapters
from .interfaces import IGroupProvider

class AnotherDynamicGroupsPlugin(DynamicGroupsPlugin):
    
    def getGroupsForPrincipal(self, principal, request=None):        
        if request is None:
            request = getRequest()
                
        groups = set()
        providers = [a for (_, a) in getAdapters((principal, request), IGroupProvider)]

        for p in providers:
            groups.update(p())
        
        return list(groups)
        