import dropbox
import tempfile
from TokenDropbox import token

dbx = dropbox.Dropbox(token)

user = dbx.users_get_current_account()

with open("twits.txt", "rb") as f:
    data = f.read()

print("Subiendo")
fname = "/datos_remotos.txt"
dbx.files_upload(data, fname, mute=True)
print("Subida Finalizada")
