# -*- coding: utf-8 -*-

from five import grok
from Products.Archetypes.interfaces import IObjectEditedEvent, IObjectInitializedEvent

from AccessControl import ClassSecurityInfo
from Products.Archetypes import atapi
from zope.interface import implements

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from vindula.streaming.config import PROJECTNAME, PATH_FILE
from vindula.streaming.content.interfaces import IVindulaStreaming

from Products.ATContentTypes.content.schemata import ATContentTypeSchema

from subprocess import Popen, PIPE
import os

StreamingSchema = ATContentTypeSchema.copy() + atapi.Schema((
    atapi.StringField(
        name='duracao',
        widget=atapi.StringField._properties['widget'](
            label="Tempo de Duração",
            description="Imforme o tempo de duração desta multimídia",
            label_msgid='LiberiunStreaming_label_duracao',
            description_msgid='LiberiunStreaming_help_duracao',
            i18n_domain='LiberiunStreaming',
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
            label_msgid='LiberiunStreaming_label_diretor',
            description_msgid='LiberiunStreaming_help_diretor',
            i18n_domain='LiberiunStreaming',
        ),
        required=False,
    ),

    atapi.FileField(
        name='video',
        required=True,
        primary=True,
        widget=atapi.FileWidget(
            label='Arquivo Multimidia',
            label_msgid='LiberiunStreaming_label_video',
            i18n_domain='LiberiunStreaming',
        ),
    ),

    atapi.ImageField(
        name='foto_video.jpg',
        widget=atapi.ImageWidget(
            label='Foto do Video',
        ),
        sizes = {'destaque.jpg' : (263,197), 'arquivo.jpg' : (131,88), 'home_box.jpg': (100,75)},
        storage=atapi.AttributeStorage(),
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

#    def at_post_create_script(self):
#        self.converte_video()

    def is_music(self):
        return self.getVideo().filename.endswith('.mp3')

    def is_video(self):
        return not self.is_music()

atapi.registerType(VindulaStreaming, PROJECTNAME)

def converte_video(objeto):

    video = str(objeto.getVideo())

    uid = objeto.UID()

    filename = PATH_FILE + uid + "_video"
    arquivo = open(filename, 'w')
    arquivo.write(video)
    arquivo.close()

    if objeto.getVideo().filename.endswith('.mp3'):
        return

    new = filename + ".flv"
    # Caso exista algum flv, apaga porque vamos gera-lo novamente
    if os.path.isfile(new):
        os.unlink(new)

    # Converte o video e seta o audio para o rate 44100
    command = ["ffmpeg", "-y", "-i", filename, "-ar", "44100", new]
    #result = Popen(command,stdout=PIPE, stderr=PIPE).communicate()
    Popen(command)
    # fecha e apaga o arquivo
    os.unlink(filename)

    #return None

@grok.subscribe(VindulaStreaming, IObjectEditedEvent)
def streaming_editado(context, event):
    converte_video(context)

@grok.subscribe(VindulaStreaming, IObjectInitializedEvent)
def streaming_adicionado(context, event):
    converte_video(context)
