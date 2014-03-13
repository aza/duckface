import json
import random

import pandas as pd
from sklearn import svm

J = json.loads(file('./json/duckface-training-export.json').read())

landmarks, labels = [], []
for k,v in J.items():
    if 'facepp_landmark_faces' in v.keys():
        #!!! No photo has more than one face. I think we may be overwriting multiple faces. Something to check.
        # print len(v['facepp_landmark_faces'])
        # print len(v['facepp_landmark_faces'][0]['result'][0])

        temp = v['facepp_landmark_faces'][0]['result'][0]['landmark']
        landmark_row = {}
        for tk, tv in temp.items():
            landmark_row[tk+"_x"] = tv["x"]
            landmark_row[tk+"_y"] = tv["y"]

        label_row = {
            "face_id" : v['facepp_landmark_faces'][0]['result'][0]['face_id'],
            "fb_key" : k,
            "url" : v['url'],
            "duckface" : v['source'] == 'instagram#duckface',
            "training" : random.uniform(0,1) < .7
        }

        landmarks.append(landmark_row)
        labels.append(label_row)

X = pd.DataFrame(landmarks)
L = pd.DataFrame(labels)
Y = L.duckface.map(int)
T = L.training

model = svm.SVC()
model.fit(X[T==1], Y[T==1])

Yhat_nt = model.predict(X[T==0])
print pd.crosstab(Y[T==0], Yhat_nt)