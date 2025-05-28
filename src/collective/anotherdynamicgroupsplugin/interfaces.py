from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IBrowserLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IGroupProvider(Interface):

    def __call__(self):
        """Return a sequence of group IDs."""
