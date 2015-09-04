# -*- coding: utf-8 -*-

from five import grok

from zope.component import getUtility, getMultiAdapter
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName

from Products.CMFCore.utils import getToolByName

from vindula.streaming.content.interfaces import IVindulaStreaming
from vindula.streaming.controlpanel import IStreamingSettings
from vindula.streaming.settings import Settings
from vindula.streaming.utils import getPortal

grok.templatedir("templates")


class StreamingView(grok.View):
    grok.context(IVindulaStreaming)
    grok.name("view")
    grok.require("zope2.View")

    enabled = True

    def update(self):
        self.registry = getUtility(IRegistry)

        self.settings = Settings(self.context)
        self.global_settings = self.registry.forInterface(IStreamingSettings)
        self.site = getPortal(self.context)

        self.portal_url = getMultiAdapter((self.context, self.request),
            name="plone_portal_state").portal_url()

        utils = getToolByName(self.context, 'plone_utils')
        msg = None

        if self.settings.converting is not None and \
                self.settings.converting:
            msg = "O arquivo está sendo convertido."
            self.enabled = False
        elif self.settings.successfully_converted is not None and \
                not self.settings.successfully_converted:
            msg = "Ocorreu um erro ao converter o arquivo. " +\
                  "Talvez o arquivo esteja corrombido ou é mal formatado." +\
                  "Cheque o log para ter mais detalhes."
            self.enabled = False
        elif self.settings.successfully_converted is None:
            # must have just switched to this view
            msg = "This document is not yet converted to document Este documento ainda não foi convertido. Por favor clique na aba `Conversor Multimídia` " +\
                  "para fazer a conversão."
            self.enabled = False

        mtool = getToolByName(self.context, 'portal_membership')
        self.can_modify = mtool.checkPermission('cmf.ModifyPortalContent',
                                                self.context)
        if msg and self.can_modify:
            utils.addPortalMessage(msg)

    def server_url(self):
        if not getattr(self, 'settings', False):
            self.update()
            
        return self.global_settings.url

    def can_download(self):
        if not getattr(self, 'settings', False):
            self.update()
            
        return self.global_settings.download

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
        
class MediaConvertView(grok.View):
    grok.context(IVindulaStreaming)
    grok.name("media-convert")
    grok.require("zope2.View")
