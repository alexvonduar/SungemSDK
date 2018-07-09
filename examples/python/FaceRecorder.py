#! /usr/bin/env python3

# Copyright(c) 2018 Senscape Corporation.
# License: Apache 2.0

# Note: This demo needs 2 HS devices

import numpy as np, cv2, sys
sys.path.append('../../api/')
import hsapi as hs
import pdb
WEBCAM = False # Set to True if use Webcam
	
net = hs.HS('FaceRec', zoom = True, verbose = 2)
net2 = hs.HS('FaceDetector', deviceIdx = 1, zoom = True, verbose = 0, threshSSD=0.55)

if WEBCAM: video_capture = cv2.VideoCapture(0)
C = 5

try:
	while True:
		if WEBCAM: _, img = video_capture.read()
		else: img = None
		
		result = net2.run(img)
		
		# Record 1st face
		key = cv2.waitKey(5)
		if len(result[1]) > 0:
			box = result[1][0]
			if box[5] - box[3] > 10 or box[4] - box[2] > 10:		
				recCrop = result[0][box[3]:box[5],box[2]:box[4],:]
				face_res = net.run(recCrop)
				prob = net.record(face_res, key, saveFilename='../misc/face.dat', numBin = C)
			
		# Recognise
		for box in result[1]:
			cropped = result[0][box[3]:box[5],box[2]:box[4],:].copy()
			face_res = net.run(cropped)
			cv2.waitKey(20)
			prob = net.record(face_res, -1, saveFilename='../misc/face.dat', numBin = C)
			if prob is not None:
				cv2.putText(result[0], '%d' % (prob.argmax() + 1), (box[2],box[3]-25), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0), 7)
				cv2.putText(result[0], '%d' % (prob.argmax() + 1), (box[2],box[3]-25), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,255), 3)
		
		img = net2.plotSSD(result)
		cv2.imshow('Detection', result[0])
		try:
			cv2.imshow('Rec', recCrop)
		except:
			pass
		cv2.waitKey(1)
finally:
	net.quit()
	net2.quit()
