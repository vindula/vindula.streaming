# -*- coding: utf-8 -*-

from zope.interface import Interface
from Products.ATContentTypes.interfaces.interfaces import ITextContent


class IVindulaStreaming(Interface, ITextContent):
    """Marker interface for VindulaStreaming
    """
