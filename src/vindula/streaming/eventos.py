# -*- coding: utf-8 -*-

import os
import cStringIO
from PIL import Image
from subprocess import Popen, PIPE

from hachoir_metadata.metadata import extractMetadata
from hachoir_parser.guess import createParser
from hachoir_core.error import HachoirError
from hachoir_core.stream import InputStreamError

from five import grok
from Products.Archetypes.interfaces import IObjectEditedEvent, IObjectInitializedEvent

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from vindula.streaming.controlpanel import IStreamingSettings
from vindula.streaming.content.vindulastreaming import VindulaStreaming


def converte_video(objeto):

    video = str(objeto.getVideo())

    uid = objeto.UID()

    registry =  getUtility(IRegistry)
    settings = registry.forInterface(IStreamingSettings)

    path = settings.path

    filename = path + uid + "_video"
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
    command = ["avconv", "-y", "-i", filename, "-ar", "44100", new]
    result = Popen(command,stdout=PIPE, stderr=PIPE).communicate()
#    Popen(command)
    # apaga o arquivo
    if os.path.isfile(new):
        os.unlink(filename)

    objeto.setDuracao(duracao(objeto))
    pega_imagem(objeto)


def metadata(objeto, key):
    uid = objeto.UID()
    registry =  getUtility(IRegistry)
    settings = registry.forInterface(IStreamingSettings)
    path = settings.path
    file = path + uid + "_video.flv"
    parser = createParser(unicode(file))
    if parser is not None:
        metadata = extractMetadata(parser)
        if metadata is not None:
            if metadata.has(key):
                return metadata.get(key)
    return None


def duracao(objeto):
    duracao = str(metadata(objeto, 'duration'))
    if duracao=='None':
        return '00:00'
    else:
        return duracao[2:7]


def random_second(objeto):
    """ Gera um tempo aleatorio de acordo com o tempo do video
    """
    import random
    #transformando em segundos
    tempo = duracao(objeto)
    arrTempo = tempo.split(":")
    if int(arrTempo[0]) < 01:
        segundos = int(arrTempo[0])*60 + int(arrTempo[1])
        segundo_aleatorio = random.randint(2, segundos)
    else:
        segundos = 60 + int(arrTempo[1])
        segundo_aleatorio = random.randint(2, segundos)
        #retorna o tempo onde sera extraido o frame
    if segundo_aleatorio >= 60:
        return "00:%02d:%02d" % (segundo_aleatorio/60, segundo_aleatorio%60)
    else:
        return "00:00:%02d" % segundo_aleatorio


def pega_imagem(objeto):
    """ Pega uma imagem do vídeo
    """
    uid = objeto.UID()

    registry =  getUtility(IRegistry)
    settings = registry.forInterface(IStreamingSettings)

    path = settings.path

    arquivo = path + uid + "_video.flv"
    imagem = path + uid + "_imagem.jpg"
    tempo = random_second(objeto)

    #verifica se existe o arquivo da imagem
    if os.path.isfile(imagem):
        os.unlink(imagem)

    comando = ["avconv", "-ss", tempo, "-i", arquivo, "-an",
               "-vsync", "1", "-vframes","1", imagem,]
    resultado = Popen(comando, stdout=PIPE, stderr=PIPE).communicate()
    if os.path.isfile(imagem):
        imagem_original = open(imagem,'r')
        img = cStringIO.StringIO(str(imagem_original.read()))
        image = Image.open(img)
        nova_imagem = cStringIO.StringIO()
        image.save(nova_imagem, image.format, quality=100)
        nova_imagem.seek(0)
        objeto.setImage(nova_imagem)
        #Apaga a imagem no filesystem
    os.unlink(imagem)

    return nova_imagem


@grok.subscribe(VindulaStreaming, IObjectEditedEvent)
def streaming_editado(context, event):
    converte_video(context)


@grok.subscribe(VindulaStreaming, IObjectInitializedEvent)
def streaming_adicionado(context, event):
    converte_video(context)
