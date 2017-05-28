import dropbox
import tempfile
import shutil
from TokenDropbox import token

dbx = dropbox.Dropbox(token)

user = dbx.users_get_current_account()

with open("twits.txt", "rb") as f:
    data = f.read()

# Subida
print("Subiendo")
fname = "/datos_remotos.txt"
dbx.files_upload(data, fname, mute=True)
print("Subida Finalizada")

# Bajada
print("Descargando")
path = "/datos_remotos.txt"
name = "twitsDescargados.txt"
file_temp = open(name,"a")
dbx.files_download_to_file(file_temp.name, path)
print("Descarga Finalizada")
