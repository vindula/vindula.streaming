# -*- coding: utf-8 -*-

from five import grok

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName

from vindula.streaming.content.interfaces import IVindulaStreaming
from vindula.streaming.controlpanel import IStreamingSettings

grok.templatedir("templates")


class StreamingView(grok.View):
    grok.context(IVindulaStreaming)
    grok.name("view")
    grok.require("zope2.View")

    def update(self):
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IStreamingSettings)

    def server_url(self):
        if not getattr(self, 'settings', False):
            self.update()
            
        return self.settings.url

    def can_download(self):
        if not getattr(self, 'settings', False):
            self.update()
            
        return self.settings.download

    def check_share(self):
        panel = self.context.restrictedTraverse('@@myvindula-conf-userpanel')
        if panel:
            return panel.check_share()


class FrameStreamingView(grok.View):
    grok.context(IVindulaStreaming)
    grok.name("frame-video-view")
    grok.require("zope2.View")

    def url_streaming(self):
        portal_url = getToolByName(self.context, "portal_url")
        portal = portal_url.getPortalObject().absolute_url()
        url = portal + '/streaming'
        return url
        