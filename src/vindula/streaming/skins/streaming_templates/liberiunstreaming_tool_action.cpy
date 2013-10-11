## Controller Python Script "liberiunstreaming_tool_action"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=
##

#Imports
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import addStatusMessage

# Tool
ltool = getToolByName(context, 'portal_liberiunstreamingtool')

#Request
request = context.REQUEST

#Pegando as variáveis passadas 
streaming_server_url = request.get('streaming_server_url', '')
streaming_files_path = request.get('streaming_files_path', '')
download_video = request.get('download_video', '')

if streaming_server_url:
    ltool.setStreaming_server_url(streaming_server_url)

if streaming_files_path:
    ltool.setStreaming_files_path(streaming_files_path)

if download_video:
    ltool.setDownload_video(True)
else:
    ltool.setDownload_video(False)
 
message = 'Alterações Salvas'
addStatusMessage(request, message)
return request.RESPONSE.redirect(ltool.absolute_url()+'/view')
