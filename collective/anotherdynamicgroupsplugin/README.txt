collective.anotherdynamicgroupsplugin
=====================================

Overview
--------

Products.PluggableAuthService provides a "Dynamic Groups Plugin". You can add "virtual" groups, and
for each of them Membership is established via a predicate, expressed as a TALES expression.

This package aims to provide a similar functionality, but in a different way. Once the 
"Another Dynamic Groups Plugin" is installed it will lookup named multi-adapters for the user and 
the request. Each adapter will provide a sequence of groups which the principal is a member of.
It's similar to `borg.localrole`_ but for groups.

This plugin is also a "groups introspection plugin". It means the "virtual" groups created are 
shown in the Plone management UI for groups. Actually, if we don't do that the 
``@@usergroup-userprefs`` view breaks.

Installation
------------

The usual: make the package available in the buildout and have its ZCML loaded. Then you can install
it as a Plone add-on into a Plone Site.

Usage
-----

Once the add-on is installed you can add "virtual" groups. These will be the groups dynamically
assigned to the users by the plugin. It also can be done through the ZMI::

    >>> from collective.anotherdynamicgroupsplugin.util import add_virtual_group
    >>> add_virtual_group(group_id='group1', title='Group 1') 
    >>> add_virtual_group(group_id='group2', title='Group 2')
    >>> add_virtual_group(group_id='group3', title='Group 3')            
    
Add some users::
    
    >>> from Products.CMFCore.utils import getToolByName
    >>> mtool = getToolByName(portal, 'portal_membership')
    >>> for u_id in ('user1', 'user2', 'user3'):
    ...     mtool.addMember(u_id, 'foo', [], [])
        
Now we create and register the named adapters. The first one just makes everybody a member of 
"group1"::

    >>> from collective.anotherdynamicgroupsplugin.interfaces import IGroupProvider
    >>> from zope.component import provideAdapter
    >>> from zope.interface import implements
    >>> from zope.publisher.interfaces.http import IHTTPRequest
    >>> from Products.PluggableAuthService.interfaces.authservice import IBasicUser
    >>> class ProvideGroup1ToAll(object):
    ...     implements(IGroupProvider)
    ...     def __init__(self, user, request):
    ...         self.user = user
    ...         self.request = request
    ...     def __call__(self):
    ...         return ['group1']
    >>> provideAdapter(ProvideGroup1ToAll, adapts=(IBasicUser, IHTTPRequest), name='provide_group1_to_all')
    
The second adapter makes the user member of the group with correspondent name::

    >>> class ProvideCorrespondentGroup(object):
    ...     implements(IGroupProvider)
    ...     def __init__(self, user, request):
    ...         self.user = user
    ...         self.request = request
    ...     def __call__(self):
    ...         if not self.user.getId().startswith('user'):
    ...             return []
    ...         number = self.user.getId()[-1]
    ...         return ['group' + number]    
    >>> provideAdapter(ProvideCorrespondentGroup, adapts=(IBasicUser, IHTTPRequest), name='provide_correspondent_group')        

Now let's check if the groups are correctly assigned to each user::

    >>> user1 = mtool.getMemberById('user1')    
    >>> sorted(user1.getGroups())
    ['AuthenticatedUsers', 'group1']
    
    >>> user2 = mtool.getMemberById('user2')    
    >>> sorted(user2.getGroups())
    ['AuthenticatedUsers', 'group1', 'group2']

    >>> user3 = mtool.getMemberById('user3')    
    >>> sorted(user3.getGroups())
    ['AuthenticatedUsers', 'group1', 'group3']

.. References
.. _`borg.localrole`: http://pypi.python.org/pypi/borg.localrole
        



