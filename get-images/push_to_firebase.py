"""
http://statigr.am/tag/duckfaces
http://statigr.am/tag/selfies

//div[@class="image-wrapper"]/a/img/@src
"""

from firebase import firebase
fb = firebase.FirebaseApplication('https://duckface.firebaseio.com/')

old = fb.get('/training', None).values()
old_urls = [row['url'] for row in old if row != None]

new_urls = file('instagram-duckface-8.txt').read().splitlines()
keep_urls = set(new_urls).difference(set(old_urls))

for i,u in enumerate(keep_urls):
    print i, u
    fb.post('/training', {'url': u, 'source': 'instagram#duckface'})


old = fb.get('/training', None).values()
old_urls = [row['url'] for row in old if row != None]

new_urls = file('instagram-selfie-8.txt').read().splitlines()
keep_urls = set(new_urls).difference(set(old_urls))

for i,u in enumerate(keep_urls):
    print i, u
    fb.post('/training', {'url': u, 'source': 'instagram#selfie'})
