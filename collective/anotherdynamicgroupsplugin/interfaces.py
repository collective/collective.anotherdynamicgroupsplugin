from zope.interface import Interface

class IGroupProvider(Interface):
    
    def __call__(self):
        """Return a sequence of group IDs."""
        