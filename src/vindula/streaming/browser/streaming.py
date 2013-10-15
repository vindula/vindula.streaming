# -*- coding: utf-8 -*-

from five import grok

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

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
        return self.settings.url

    def can_download(self):
        return self.settings.download
