# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from zope import schema
from zope.interface import Interface


class IStreamingSettings(Interface):
    """ Interface para o painel de controle do produto
    """

    path = schema.TextLine(
        title=u"Caminho dos arquivos no servidor de streaming",
        description=u"Informe o caminho fisico (filesystem) de onde os arquivos no servidor de Streaming",
        required=True
    )

    url = schema.TextLine(
        title=u"URL do servidor de streaming",
        description=u"Informe a URL do servidor de streaming",
        required=True
    )

    download = schema.Bool(
        title=u"Download video",
        description=u"Marcar esta opção para permitir download dos videos",
        required=False,
        default=True
    )

class StreamingSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IStreamingSettings
    label = u"Configuração do Vindula Streaming"
    description = u"Configuração do Vindula Streaming"

    def updateFields(self):
        super(StreamingSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(StreamingSettingsEditForm, self).updateWidgets()


class StreamingSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = StreamingSettingsEditForm
