import json
import glob
import re

G = glob.glob('json/*.json')

for g in G:
    L = file(g).readlines()
    # print len(L)
    for l in L:
        try:
            if re.search( 'media', l ):
                j = json.loads(l)
                print j[0]["media_url_https"]
        
        except IndexError:
            pass

        except KeyError:
            pass



# url
# fpp_json
