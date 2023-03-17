from raspagem import get_discos
from raspagemYoutube import return_albuns_links
import json


with open('discos.json', 'w', encoding='utf8') as file:
    json_archive = json.dump(get_discos(400), file, ensure_ascii=False)
    file.write(json_archive)
return_albuns_links()
