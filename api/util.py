#! /usr/bin/env python3

# Copyright(c) 2018 Senscape Corporation.
# License: Apache 2.0

# box(x1,y1,x2,y2,score)
import numpy as np

### DETECTION RELATED ###

# Detection bounding box NMS filter
# Return valid indices
def detNMS(boxes, threshold, mode='union'):
	x1 = boxes[:, 2]
	y1 = boxes[:, 3]
	x2 = boxes[:, 4]
	y2 = boxes[:, 5]
	scores = boxes[:, 1]
	areas = (x2 - x1 + 1) * (y2 - y1 + 1)
	order = scores.argsort()[::-1]
	keep = []
	while order.size > 0:
		i = order[0]
		keep.append(i)
		xx1 = np.maximum(x1[i], x1[order[1:]])
		yy1 = np.maximum(y1[i], y1[order[1:]])
		xx2 = np.minimum(x2[i], x2[order[1:]])
		yy2 = np.minimum(y2[i], y2[order[1:]])
		w = np.maximum(0.0, xx2 - xx1 + 1)
		h = np.maximum(0.0, yy2 - yy1 + 1)
		inter = w * h
		if mode == 'union':
			ovr = inter / (areas[i] + areas[order[1:]] - inter)
		elif mode == 'min':
			ovr = inter / np.minimum(areas[i], areas[order[1:]])
		else:
			raise TypeError('Unknown nms mode: %s.' % mode)
		inds = np.where(ovr <= threshold)[0]
		order = order[inds + 1]

	return keep
	
# Padding bounding boxes
def detPadding(bboxes, im_height, im_width):
	bboxes = np.array(bboxes)
	bboxes[:, 2] = np.maximum(0, bboxes[:, 2])
	bboxes[:, 3] = np.maximum(0, bboxes[:, 3])
	bboxes[:, 4] = np.minimum(im_width - 1, bboxes[:, 4])
	bboxes[:, 5] = np.minimum(im_height - 1, bboxes[:, 5])
	return bboxes

# Make bounding boxes square
def detBox2Square(bboxes):
	bboxes = np.array(bboxes)
	square_bbox = bboxes.copy()
	w = bboxes[:, 4] - bboxes[:, 2] + 1
	h = bboxes[:, 5] - bboxes[:, 3] + 1
	max_side = np.maximum(h, w)
	square_bbox[:, 2] = bboxes[:, 2] + (w - max_side) * 0.5
	square_bbox[:, 3] = bboxes[:, 3] + (h - max_side) * 0.5
	square_bbox[:, 4] = square_bbox[:, 2] + max_side - 1
	square_bbox[:, 5] = square_bbox[:, 3] + max_side - 1
	return square_bbox
	

