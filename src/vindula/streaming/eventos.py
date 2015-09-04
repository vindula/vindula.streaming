# -*- coding: utf-8 -*-
import cStringIO
import os
from subprocess import Popen, PIPE
import traceback
from DateTime import DateTime
from PIL import Image
from hachoir_metadata.metadata import extractMetadata
from hachoir_parser.guess import createParser
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

from vindula.streaming.async import queueJob
from vindula.streaming.controlpanel import IStreamingSettings
from vindula.streaming.settings import Settings


def converte_video(objeto):

    settings = Settings(objeto)
    try:
        video = str(objeto.getVideo())

        uid = objeto.UID()

        registry =  getUtility(IRegistry)
        global_settings = registry.forInterface(IStreamingSettings)

        path = global_settings.path

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

        settings.successfully_converted = True
    except Exception, ex:
        settings.successfully_converted = False
        settings.exception_msg = getattr(ex, 'message', '')
        settings.exception_traceback = traceback.format_exc()

    settings.last_updated = DateTime().ISO8601()
    settings.converting = False

    objeto.setDuracao(duracao(objeto))
    pega_imagem(objeto)


def metadata(objeto, key):
    uid = objeto.UID()
    registry =  getUtility(IRegistry)
    global_settings = registry.forInterface(IStreamingSettings)
    path = global_settings.path
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
    global_settings = registry.forInterface(IStreamingSettings)

    path = global_settings.path

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

# @grok.subscribe(VindulaStreaming, IObjectEditedEvent)
# def streaming_editado(context, event):
#     queueJob(context)
#     # converte_video(context)


# @grok.subscribe(VindulaStreaming, IObjectInitializedEvent)
def streaming_adicionado(context, event):
    queueJob(context)
    # converte_video(context)
