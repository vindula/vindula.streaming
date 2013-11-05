.. contents::

Integracao - Plone com Nginx
============================

Para otimizar a arquitetura da aplicação e evitar que as threads do Plone
ficassem ocupadas servindo os arquivos de áudio e de vídeo, utilizamos
a tecnologia de streaming para eliminar qualquer problema ao exibir os 
conteúdos de mídia, tornando a aplicacao mais rapida e inteligente.
Utilizamos as seguintes tecnologias:
    
    - Plone 4.3
    - Zope3 views
    - Servidor web Nginx
    - Programa avconv para fazer a conversao do video para flv

Ao instalar o produto vindula.streaming, é necessário configurar o painel
de controle do produto informando qual o endereço web que irá servir o
arquivo do streaming e o path do servidor onde serão armazenados os arquivos
após a conversão.

O path é o local onde o Nginx irá servir os arquivos.

No vindula, geralmente, o path ficará em:

/opt/intranet/frontend/nginx/templates/html/streaming/

Informando este caminho, o sistema irá converter os arquivos de mídia e 
colocá-los neste local.

É necessário configurar o Nginx para servir os arquivos de mídia. Para isso,
insira as seguintes linhas dentro da diretiva *server* do Nginx:

    location /streaming {
        root  /opt/intranet/frontend/nginx/templates/html;
    }

Após essas configurações o sistema estará pronto para servir streaming.
