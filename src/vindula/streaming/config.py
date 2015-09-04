# -*- coding: utf-8 -*-

PROJECTNAME = 'vindula.streaming'

ADD_PERMISSIONS = {
    'VindulaStreaming': 'vindula.streaming: Add VindulaStreaming',
    }

class DocType(object):

    def __init__(self, name, extensions, requires_conversion=True):
        self.name = name
        self.extensions = extensions
        self.requires_conversion = requires_conversion

CONVERTABLE_TYPES = {
    'pdf': DocType(u'PDF', ('pdf',), False),
    'word': DocType(u'Word Document', ('doc', 'docx', 'odt', 'sxw',
                                       'wks', 'wpd', 'vor', 'sdw')),
    'excel': DocType(u'Excel File', ('xls', 'xlsx', 'xlt', 'ods')),
    'ppt': DocType(u'Powerpoint', ('ppt', 'pptx', 'pps', 'ppa', 'pwz',
                                  'odp', 'sxi')),
    'html': DocType(u'HTML File', ('htm', 'html', 'xhtml')),
    'rft': DocType(u'RTF', ('rtf',)),
    'ps': DocType(u'PS Document', ('ps', 'eps', 'ai')),
    'photoshop': DocType(u'Photoshop', ('psd',)),
    'visio': DocType(u'Visio', ('vss', 'vst', 'vsw', 'vsd')),
    'palm': DocType(u'Aportis Doc Palm', ('pdb',)),
}

EXTENSION_TO_ID_MAPPING = {}
