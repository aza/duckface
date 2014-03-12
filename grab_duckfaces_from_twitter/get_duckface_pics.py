import json
import twitter

import auth

api = twitter.Api(
    consumer_key=auth.consumer_key,
    consumer_secret=auth.consumer_secret,
    access_token_key=auth.access_token,
    access_token_secret=auth.access_token_secret
)

last_id = None
for x in range(100):
    # A = api.GetSearch("#duckface", include_entities=True, count=100, max_id=last_id)
    A = api.GetSearch("#selfie", include_entities=True, count=100, max_id=last_id)
    U = [a.media[0]["media_url"] for a in A if a.media != []]
    last_id = A[-1].AsDict()['id']

    tweetfile = file('json/tweets-'+str(last_id)+'.json', 'w')
    mediafile = file('json/media-'+str(last_id)+'.json', 'w')
    for a in A:
        tweetfile.write(json.dumps(a.AsDict())+'\n')
        if a.media != []:
            mediafile.write(json.dumps(a.media)+'\n')


