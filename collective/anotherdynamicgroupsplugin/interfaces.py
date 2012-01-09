from zope.interface import Interface

class IGroupProvider(Interface):
    
    def __call__(self):
        pass