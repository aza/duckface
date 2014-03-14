import json
import random

import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.linear_model import LogisticRegression
import pylab as plt

J = json.loads(file('./json/duckface-training-export.json').read())

landmarks, labels = [], []
for k,v in J.items():
    if 'facepp_landmark_faces' in v.keys():
        # assert False
        #!!! No photo has more than one face. I think we may be overwriting multiple faces. Something to check.
        # print len(v['facepp_landmark_faces'])
        # print len(v['facepp_landmark_faces'][0]['result'][0])

        for i in v['facepp_landmark_faces']: 
            # temp = v['facepp_landmark_faces'][0]['result'][0]['landmark']
            # print i
            temp = i['result'][0]['landmark']

            landmark_row = {}
            for tk, tv in temp.items():
                landmark_row[tk+"_x"] = tv["x"]
                landmark_row[tk+"_y"] = tv["y"]

            label_row = {
                # "face_id" : v['facepp_landmark_faces'][0]['result'][0]['face_id'],
                "face_id" : i['result'][0]['face_id'],
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

check_points = [
    'contour_chin',
    'mouth_left_corner',
    'mouth_lower_lip_bottom',
    # 'mouth_lower_lip_left_contour1',
    'mouth_lower_lip_left_contour2',
    # 'mouth_lower_lip_left_contour3',
    # 'mouth_lower_lip_right_contour1',
    'mouth_lower_lip_right_contour2',
    # 'mouth_lower_lip_right_contour3',
    'mouth_lower_lip_top',
    'mouth_right_corner',
    'mouth_upper_lip_bottom',
    'mouth_upper_lip_left_contour1',
    # 'mouth_upper_lip_left_contour2',
    'mouth_upper_lip_left_contour3',
    'mouth_upper_lip_right_contour1',
    # 'mouth_upper_lip_right_contour2',
    'mouth_upper_lip_right_contour3',
    'mouth_upper_lip_top',
    # 'nose_contour_left1',
    # 'nose_contour_left2',
    # 'nose_contour_left3',
    'nose_contour_lower_middle',
    # 'nose_contour_right1',
    # 'nose_contour_right2',
    # 'nose_contour_right3',
    'nose_left',
    'nose_right',
    'nose_tip'
]

check_points = [
    'contour_chin',
    'mouth_lower_lip_bottom',
    'mouth_upper_lip_top',
    'nose_tip',
]

for i,p in enumerate(check_points):
    for q in check_points[i+1:]:
        X["dist_"+p+"_"+q] = np.sqrt((X[p+'_x']-X[q+'_x'])**2 + (X[p+'_y']-X[q+'_y'])**2)

X2 = X[[x for x in list(X) if x[:5]=='dist_']]
# X2_norm = X2.apply(lambda row: row/row.sum(), axis=1)

model = LogisticRegression()
model.fit(X2[T==1], Y[T==1])

Yhat_nt = model.predict(X2[T==0])
proby_nt = model.predict_proba(X2[T==0])
x = pd.crosstab(Y[T==0], Yhat_nt)

print x
print (x[0][0]+x[1][1])*1./x.sum().sum()
y = Y[T==0].mean()
print y*y + (1-y)*(1-y)


model = svm.SVC(kernel='rbf')
# model = svm.LinearSVC()
model.fit(X2[T==1], Y[T==1])

Yhat_nt = model.predict(X2[T==0])
x = pd.crosstab(Y[T==0], Yhat_nt)

print x
print (x[0][0]+x[1][1])*1./x.sum().sum()
y = Y[T==0].mean()
print y*y + (1-y)*(1-y)


