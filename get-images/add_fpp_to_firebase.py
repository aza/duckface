import json
import requests

from firebase import firebase

facepp_key = '83c6d84242b88722bbd88bb2000af93e'
facepp_secret = 'Tuoci57URDmmzD_IArfn3xSVxziVGb9K'
facepp_detect_url = 'http://apius.faceplusplus.com/v2/detection/detect'
facepp_landmark_url = 'http://apius.faceplusplus.com/v2/detection/landmark'

fb = firebase.FirebaseApplication('https://duckface.firebaseio.com/')

photo_dict = fb.get('/training', None)

count = 0
for fb_key, photo in photo_dict.items():
    print count, fb_key
    new_photo = photo.copy()

    if not 'facepp_detect' in photo:
        r = requests.post(facepp_detect_url, data={
            'api_key': facepp_key,
            'api_secret': facepp_secret,
            'url': photo['url']
        })

        new_photo['facepp_detect'] = r.content

    if ('face' in new_photo['facepp_detect']) and (not 'facepp_landmark_faces' in new_photo):
        new_photo['facepp_landmark_faces'] = []

        for face in new_photo['facepp_detect']['face']:
            r = requests.post(facepp_landmark_url, data={
                'api_key': facepp_key,
                'api_secret': facepp_secret,
                'face_id': face['face_id']
            })

        new_photo['facepp_landmark_faces'].append(json.loads(r.content))

    if photo != new_photo:
        # print json.dumps(photo, indent=2)
        # print json.dumps(new_photo, indent=2)
        # print photo.keys()
        # print new_photo.keys()
        # print fb_key

        photo_dict = fb.patch('/training/'+fb_key, new_photo)

    for k in photo.keys():
        if not k in ['url', 'source', 'facepp_detect', 'facepp_landmark_faces']:
            print k
            print '/training/'+fb_key+'/'+k
            photo_dict = fb.delete('/training/'+fb_key+'/'+k, None)

    count += 1
