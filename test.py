import requests
from PIL import Image
from io import BytesIO
from cachecontrol import CacheControl

"""
from helpers import *


print(wiki_search("Albert Einst"))
"""

r = requests.get("https://upload.wikimedia.org/wikipedia/en/0/09/Demon_Slayer_-_Kimetsu_no_Yaiba%2C_volume_1.jpg")
i = Image.open(BytesIO(r.content))
print(i.show())

