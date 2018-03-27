# Trabajo-Final-SD
### Knowledge Discovery in Twitter's  Databases
Trabajo final de la asignatura Sistemas Distribuidos.

## Miembros del grupo:
- **Juan Francisco Cabrera Sánchez** - *Github profile* - [JF95](https://github.com/JF95)
- **Carlos Gallardo Polanco** - *Github profile* - [gpcarlos](https://github.com/gpcarlos)

## Descripción:
  El programa ofrece diferentes estadísticas y archivos .xls en base a los
  tweets encontrados en un periodo de tiempo, basados en los términos
  introducidos por el usuario.

![Preview](/Screen.png)

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
      token = ' añada aqui los token correspondientes '
      ----------------------

  Una vez hecho ésto ejecute el servidor:
    ```
    $ python Servidor.py
    ```

  Luego el cliente:
    ```
    $ python Cliente.py
    ```

  Tras esto, introduzca los términos que quiera uno a uno y pulsando 'Añadir'.
  Haga lo mismo con el tiempo en minutos (por defecto está a 0.2 minutos).

  Pulse 'Capturar' y espere.

  Cuando termine, pulse 'Procesar' y seleccione qué gráfica quiere ver:
  Impacto, Idiomas o Medios.

  Tras esto encontrará en Dropbox los archivos .json .xls y .png de las
  gráficas que haya seleccionado.

### ¡Cuidado!

  Para que todo funcione correctamente, cada vez que quiera probar el programa debe asegurarse de que la carpeta de Dropbox en la que se suben los archivos está vacía y que ha borrado los .json que pueda haber en la carpeta en la que está Cliente.py. En caso contrario se pueden mezclar los tweets nuevos con tweets antiguos.
