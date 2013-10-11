from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class VindulastreamingLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import vindula.streaming
        xmlconfig.file(
            'configure.zcml',
            vindula.streaming,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'vindula.streaming:default')

VINDULA_STREAMING_FIXTURE = VindulastreamingLayer()
VINDULA_STREAMING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(VINDULA_STREAMING_FIXTURE,),
    name="VindulastreamingLayer:Integration"
)
VINDULA_STREAMING_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VINDULA_STREAMING_FIXTURE, z2.ZSERVER_FIXTURE),
    name="VindulastreamingLayer:Functional"
)
