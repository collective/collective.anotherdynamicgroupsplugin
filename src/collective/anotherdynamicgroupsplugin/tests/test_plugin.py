from collective.anotherdynamicgroupsplugin.interfaces import IGroupProvider
from collective.anotherdynamicgroupsplugin.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.PluggableAuthService.interfaces.authservice import IBasicUser
from zope.component import provideAdapter
from zope.interface import implementer
from zope.publisher.interfaces.http import IHTTPRequest

import unittest


@implementer(IGroupProvider)
class ProvideGroup1ToAll:

    def __init__(self, user, request):
        self.user = user
        self.request = request

    def __call__(self):
        return ["group1"]


@implementer(IGroupProvider)
class ProvideCorrespondentGroup:

    def __init__(self, user, request):
        self.user = user
        self.request = request

    def __call__(self):
        if not self.user.getId().startswith("user"):
            return []
        number = self.user.getId()[-1]
        return ["group" + number]


class TestPlugin(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        from collective.anotherdynamicgroupsplugin.util import add_virtual_group

        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        # add two virtual groups
        add_virtual_group(group_id="group1", title="Group 1")
        add_virtual_group(group_id="group2", title="Group 2")

        # add a regular group
        api.group.create(groupname="group3", title="Group 3")

        # add some users
        for u_id in ("user1", "user2", "user3"):
            api.user.create(username=u_id, email=u_id + "@test.org")

        # register adapter
        provideAdapter(
            ProvideGroup1ToAll,
            adapts=(IBasicUser, IHTTPRequest),
            name=ProvideGroup1ToAll.__name__,
        )

        # register adapter
        provideAdapter(
            ProvideCorrespondentGroup,
            adapts=(IBasicUser, IHTTPRequest),
            name=ProvideCorrespondentGroup.__name__,
        )

    def test_add_virtual_group(self):
        from collective.anotherdynamicgroupsplugin import PLUGIN_ID

        pas = api.portal.get_tool("acl_users").get(PLUGIN_ID)
        self.assertIn("group1", pas.listGroupIds())
        self.assertIn("group2", pas.listGroupIds())
        self.assertNotIn("group3", pas.listGroupIds())

    def test_registered_adapters(self):
        from zope.component import getGlobalSiteManager

        sm = getGlobalSiteManager()
        adapter_names = [adapter.name for adapter in list(sm.registeredAdapters())]

        self.assertIn(ProvideGroup1ToAll.__name__, adapter_names)
        self.assertIn(ProvideCorrespondentGroup.__name__, adapter_names)

    def test_unregister_adapters(self):
        from zope.component import getGlobalSiteManager

        sm = getGlobalSiteManager()

        for a in (ProvideGroup1ToAll, ProvideCorrespondentGroup):
            sm.unregisterAdapter(
                provided=IGroupProvider,
                required=(IBasicUser, IHTTPRequest),
                name=a.__name__,
            )

        adapter_names = [adapter.name for adapter in list(sm.registeredAdapters())]
        self.assertNotIn(ProvideGroup1ToAll.__name__, adapter_names)
        self.assertNotIn(ProvideCorrespondentGroup.__name__, adapter_names)

    def test_user_to_groups(self):

        user1_groups = sorted(g.getId() for g in api.group.get_groups(username="user1"))
        self.assertListEqual(["AuthenticatedUsers", "group1"], user1_groups)

        user2_groups = sorted(g.getId() for g in api.group.get_groups(username="user2"))
        self.assertListEqual(["AuthenticatedUsers", "group1", "group2"], user2_groups)

        user3_groups = sorted(g.getId() for g in api.group.get_groups(username="user3"))
        self.assertListEqual(["AuthenticatedUsers", "group1", "group3"], user3_groups)

    def test_getGroupIds(self):
        from collective.anotherdynamicgroupsplugin import PLUGIN_ID

        pas = api.portal.get_tool("acl_users").get(PLUGIN_ID)
        groups = pas.getGroupIds()
        self.assertListEqual(groups, ["group1", "group2"])

    def test_getGroupMembers(self):
        # getGroupMembers returns always a empty list
        # not implemented --> method are suspect for scalability ?
        from collective.anotherdynamicgroupsplugin import PLUGIN_ID

        pas = api.portal.get_tool("acl_users").get(PLUGIN_ID)
        members = pas.getGroupMembers("group1")
        self.assertListEqual(members, [])
