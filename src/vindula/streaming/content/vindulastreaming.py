# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from Products.Archetypes import atapi
from zope.interface import implements

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from vindula.streaming.config import PROJECTNAME
from vindula.streaming.content.interfaces import IVindulaStreaming

from Products.ATContentTypes.content.schemata import ATContentTypeSchema

from vindula.content.models.content_field import ContentField

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
                                                             
    atapi.LinesField(
        'themesNews',
        multiValued=1,
        accessor="ThemeNews",
        searchable=True,
        schemata='categorization',
        widget=atapi.KeywordWidget(
            label='Temas',
            description='Selecione os temas.',
        ),
    ),
                                                             
    atapi.StringField(
        name='tipo',
        searchable = True,
        widget = atapi.SelectionWidget(
            label="Tipologia",
            description="Selecione a tipologia do vídeo.",
            format = 'select', 
        ),
        vocabulary='get_tipo',
    ), 

    atapi.BooleanField(
        name='activ_share',
        default=True,
        widget=atapi.BooleanWidget(
            label="Ativar barra social",
            description='Caso selecionado, ativa a barra social.',
        ),
        required=False,
        schemata='settings',
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
    
    def get_tipo(self):
        content_fields = ContentField().get_content_file_by_type(u'tipo')
        L = [('', '-- Selecione --')]
        for item in content_fields:
            L.append((item,item))
            
        return atapi.DisplayList(tuple(L))

atapi.registerType(VindulaStreaming, PROJECTNAME)