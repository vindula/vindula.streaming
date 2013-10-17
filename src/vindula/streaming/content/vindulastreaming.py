# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from Products.Archetypes import atapi
from zope.interface import implements

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from vindula.streaming.config import PROJECTNAME
from vindula.streaming.content.interfaces import IVindulaStreaming

from Products.ATContentTypes.content.schemata import ATContentTypeSchema

StreamingSchema = ATContentTypeSchema.copy() + atapi.Schema((
    atapi.StringField(
        name='duracao',
        widget=atapi.StringField._properties['widget'](
            label="Tempo de Duração",
            description="Imforme o tempo de duração desta multimídia",
        ),
        required=True,
    ),

    atapi.StringField(
        name='ano',
        widget=atapi.StringField._properties['widget'](
            label="Ano da Multimídia",
            description="Imforme o ano desta multimídia",
        ),
        required=False,
    ),

    atapi.StringField(
        name='diretor',
        widget=atapi.StringField._properties['widget'](
            label="Diretor",
            description="Se for um vídeo informe o diretor",
        ),
        required=False,
    ),

    atapi.FileField(
        name='video',
        required=True,
        primary=True,
        widget=atapi.FileWidget(
            label='Arquivo Multimidia',
        ),
    ),

    atapi.ImageField(
        name='image',
        widget=atapi.ImageWidget(
            label='Foto do Video',
        ),
        sizes= {'large'   : (768, 768),
                'preview' : (400, 400),
                'mini'    : (200, 200),
                'thumb'   : (128, 128),
                'tile'    :  (64, 64),
                'icon'    :  (32, 32),
                'listing' :  (16, 16),
                },
    ),
),)

StreamingSchema['description'].schemata='default'


class VindulaStreaming(atapi.BaseContent, BrowserDefaultMixin):
    """
    """

    security = ClassSecurityInfo()
    implements(IVindulaStreaming)

    meta_type = 'VindulaStreaming'
    _at_rename_after_creation = True

    schema = StreamingSchema

    def is_music(self):
        return self.getVideo().filename.endswith('.mp3')

    def is_video(self):
        return not self.is_music()

atapi.registerType(VindulaStreaming, PROJECTNAME)
