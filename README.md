# collective.anotherdynamicgroupsplugin

## Overview

Products.PluggableAuthService provides a "Dynamic Groups Plugin". You can add "virtual" groups, and
for each of them Membership is established via a predicate, expressed as a TALES expression.

This package aims to provide a similar functionality, but in a different way. Once the
"Another Dynamic Groups Plugin" is installed it will lookup registered group providers (technically
these are named multi-adapters for the user and the request). Each group provider will provide a
set of groups which the user is a member of. It's similar to `borg.localrole`_ but for
groups.

> **_NOTE:_**  A group provider can also provide membership for regular (non-virtual) groups.

The provided plugin is also a "groups introspection plugin". It means the "virtual" groups created
are shown in the Plone management UI for groups. Actually, if we don't do that the
``@@usergroup-userprefs`` view breaks.

## Compatibility

Current version was tested with Plone 6.

## Installation

**pip based:**

```
pip install collective.anotherdynamicgroupsplugin
```

**buildout based:**

The usual: make the package available in the buildout and have its ZCML loaded. Then you can install it as a Plone add-on into a Plone Site.

## Usage

Once the add-on is installed you can add "virtual" groups. These will be the groups dynamically
assigned to the users by the plugin. This can also be done through the ZMI

Now we create and register the named adapters. The first one just makes everybody a member of
"group1"

### Examples

**Example - all users are in a dynamic group**

You can register the adapter either full in python code or via zcml file.

register the full adapter in python code:

``` python

    from collective.anotherdynamicgroupsplugin.interfaces import IGroupProvider
    from zope.component import provideAdapter
    from zope.interface import implementer
    from zope.publisher.interfaces.http import IHTTPRequest
    from Products.PluggableAuthService.interfaces.authservice import IBasicUser

    @implementer(IGroupProvider)
    class ProvideGroup1ToAll(object):

        def __init__(self, user, request):
            self.user = user
            self.request = request

        def __call__(self):
            # all users are in group1
            return ['group1']

    provideAdapter(
        ProvideGroup1ToAll,
        adapts=(IBasicUser, IHTTPRequest),
        name="ProvideGroup1ToAll"
    )
```

**OR** register your named adapter via zcml:

`configure.zcml`

``` xml
    <!-- register the named adapters in your configure.zcml -->
    <adapter factory=".dynamic_groups.ProvideGroup1ToAll" name="ProvideGroup1ToAll" />
```

with this adapter registration snippet in zcml, your code should be looks like so:

`dynamic_groups.py`

``` python

    from collective.anotherdynamicgroupsplugin.interfaces import IGroupProvider
    from zope.component import adapter
    from zope.interface import implementer
    from zope.publisher.interfaces.http import IHTTPRequest
    from Products.PluggableAuthService.interfaces.authservice import IBasicUser

    @implementer(IGroupProvider)
    @adapter(IBasicUser, IHTTPRequest)
    class ProvideGroup1ToAll(object):

        def __init__(self, user, request):
            self.user = user
            self.request = request

        def __call__(self):
            # all users are in group1
            return ['group1']
```
