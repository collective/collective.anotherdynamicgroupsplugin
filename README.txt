collective.anotherdynamicgroupsplugin
=====================================

Overview
--------

Products.PluggableAuthService provides a "Dynamic Groups Plugin". You can add "virtual" groups, and
for each of them Membership is established via a predicate, expressed as a TALES expression.

This package aims to provide a similar functionality, but in a different way. Once the
"Another Dynamic Groups Plugin" is installed it will lookup registered group providers (technicaly
these are named multi-adapters for the user and the request). Each group provider will provide a
set of groups which the user is a member of. It's similar to `borg.localrole`_ but for
groups.

.. NOTE::
   A group provider can also provide membership for regular (non-virtual) groups.

The provided plugin is also a "groups introspection plugin". It means the "virtual" groups created
are shown in the Plone management UI for groups. Actually, if we don't do that the
``@@usergroup-userprefs`` view breaks.

Compatibility
-------------

Current version was tested with Plone 4.3. Probably it will work for any version in the 4.x series.

Installation
------------

The usual: make the package available in the buildout and have its ZCML loaded. Then you can install
it as a Plone add-on into a Plone Site.

Usage
-----

Once the add-on is installed you can add "virtual" groups. These will be the groups dynamically
assigned to the users by the plugin. This can also be done through the ZMI::

    >>> from collective.anotherdynamicgroupsplugin.util import add_virtual_group
    >>> add_virtual_group(group_id='group1', title='Group 1')
    >>> add_virtual_group(group_id='group2', title='Group 2')

We'll also add a regular group, since group providers can assign users to these too::

    >>> from plone import api
    >>> api.group.create(groupname='group3', title='Group 3')
    <GroupData ...

Add some users::

    >>> for u_id in ('user1', 'user2', 'user3'):
    ...     api.user.create(username=u_id, email=u_id + '@test.org')
    <MemberData ...
    <MemberData ...
    <MemberData ...

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
    >>> provideAdapter(
    ...     ProvideGroup1ToAll,
    ...     adapts=(IBasicUser, IHTTPRequest),
    ...     name=ProvideGroup1ToAll.__name__
    ... )

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
    >>> provideAdapter(
    ...     ProvideCorrespondentGroup,
    ...     adapts=(IBasicUser, IHTTPRequest),
    ...     name=ProvideCorrespondentGroup.__name__
    ... )

Now let's check if the groups are correctly assigned to each user::

    >>> sorted(g.getId() for g in api.group.get_groups(username='user1'))
    ['AuthenticatedUsers', 'group1']

    >>> sorted(g.getId() for g in api.group.get_groups(username='user2'))
    ['AuthenticatedUsers', 'group1', 'group2']

    >>> sorted(g.getId() for g in api.group.get_groups(username='user3'))
    ['AuthenticatedUsers', 'group1', 'group3']

Test clean-up::

    >>> from zope.component import getGlobalSiteManager
    >>> sm = getGlobalSiteManager()
    >>> for a in (ProvideGroup1ToAll, ProvideCorrespondentGroup):
    ...     removed = sm.unregisterAdapter(
    ...         provided=IGroupProvider,
    ...         required=(IBasicUser, IHTTPRequest),
    ...         name=a.__name__
    ...     )
    >>> list(sm.registeredAdapters())
    []


.. References
.. _`borg.localrole`: http://pypi.python.org/pypi/borg.localrole




