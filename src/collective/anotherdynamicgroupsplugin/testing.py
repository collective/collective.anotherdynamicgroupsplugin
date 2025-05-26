from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer


class PackageLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.anotherdynamicgroupsplugin

        self.loadZCML(package=collective.anotherdynamicgroupsplugin)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, "collective.anotherdynamicgroupsplugin:default")


FIXTURE = PackageLayer()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="collective.anotherdynamicgroupsplugin:Integration"
)
