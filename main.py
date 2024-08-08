import sys
from pathlib import Path

from download import download
from magnet import find_best_match
from seedr.account import SeedrAccount
from seedr.path import SeedrFolder

target = Path("/sdcard/Download")


query = sys.argv[1]
magnet = find_best_match(query)
account = SeedrAccount()
folder_id = account.add_torrent(magnet)
folder = SeedrFolder(folder_id)
for file in folder.traverse():
    url = file.url
    path = target / file.path
    download(url, path)
