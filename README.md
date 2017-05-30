# Trabajo-Final-SD
Trabajo final de la asignatura Sistemas Distribuidos.

## Miembros del grupo:
  · Juan Francisco Cabrera Sánchez
  · Carlos Gallardo Polanco

## Descripción:
  El programa ofrece diferentes estadísticas y archivos .xls en base a los
  tweets encontrados en un periodo de tiempo, basados en los términos
  introducidos por el usuario.

## ¿Cómo ejecutarlo?
  Antes de nada, descargue sus tokens de Dropbox y Twitter.
  Almacenelos en los ficheros Token_Dropbox.py y Token_Twitter.py
  en el mismo directorio y de la siguiente forma:

      Contenido de Token_Twitter.py:
      ----------------------
      consumer_key = ' añada aqui los token correspondientes '
      consumer_secret = ' añada aqui los token correspondientes '
      access_key = ' añada aqui los token correspondientes '
      access_secret = ' añada aqui los token correspondientes '
      ----------------------

      Contenido de Token_Dropbox.py:
      ----------------------
      token=' añada aqui los token correspondientes '
      ----------------------

  Una vez hecho ésto ejecute el servidor:
    '''
    $ python Servidor.py
    '''

  Luego el cliente:
    '''
    $ python Cliente.py
    '''

  Tras esto, introduzca los términos que quiera uno a uno y pulsando 'Añadir'.
  Haga lo mismo con el tiempo en minutos (por defecto está a 0.2 minutos).

  Pulse 'Capturar' y espere.

  Cuando termine, pulse 'Procesar' y seleccione qué gráfica quiere ver:
  Impacto, Idiomas o Medios.

  Tras esto encontrará en Dropbox los archivos .json .xls y .png de las
  gráficas que haya seleccionado.
