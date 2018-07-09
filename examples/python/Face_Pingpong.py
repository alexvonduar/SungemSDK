#! /usr/bin/env python3

# Copyright(c) 2018 Senscape Corporation.
# License: Apache 2.0

import numpy as np, cv2, sys
sys.path.append('../../api/')
import hsproc

# GUI
import kivy
kivy.require('1.10.0') # replace with your current kivy version !
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
	ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Color
from kivy.graphics.texture import Texture
from random import randint

class Face(Widget):
	def getImg(self, img):
		self.texture.blit_buffer(img, colorfmt='rgb', bufferfmt='ubyte')

class PongPaddle(Widget):
	
	score = NumericProperty(0)
	r = NumericProperty(0)
	
	def bounce_ball(self, ball):
		if self.collide_widget(ball):
			vx, vy = ball.velocity
			offset = (ball.center_y - self.center_y) / (self.height / 2)
			bounced = Vector(-1 * vx, vy)
			vel = bounced * 1.1
			ball.velocity = vel.x, vel.y + offset

	def change_color(self, active):
		if active:
			self.r = 0
		else:
			self.r = 1

class PongBall(Widget):
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(0)
	velocity = ReferenceListProperty(velocity_x, velocity_y)

	def move(self):
		self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
	ball = ObjectProperty(None)
	player1 = ObjectProperty(None)
	player2 = ObjectProperty(None)

	FaceDet = hsproc.HSProc('FaceDetector', False, zoom=True, verbose=0, threshSSD=0.5)
	boxes = None
	imsize = None
	displayFace = True

	def serve_ball(self, vel=(5, 0)):
		self.ball.center = self.center
		self.ball.velocity = vel

	def update(self, dt):
		try:
			ret = self.FaceDet.res_queue.get(False)
			dispImg = self.FaceDet.net.plotSSD(ret)
			self.imsize = dispImg.shape
			self.boxes = ret[1]
			
			if self.displayFace:
				dispImg = cv2.flip(dispImg, 1)
				cv2.imshow("Face Detector", dispImg)
				cv2.waitKey(1)
		except:
			pass

		self.ball.move()

		# bounce of paddles
		self.player1.bounce_ball(self.ball)
		self.player2.bounce_ball(self.ball)

		# bounce ball off bottom or top
		if (self.ball.y < self.y) or (self.ball.top > self.top):
			self.ball.velocity_y *= -1

		# went of to a side to score point?
		if self.ball.x < self.x:
			self.player2.score += 1
			self.serve_ball(vel=(10, 0))
		if self.ball.x > self.width:
			self.player1.score += 1
			self.serve_ball(vel=(-10, 0))
			
		self.player1.change_color(False)
		self.player2.change_color(False)
		
		if self.boxes is not None:
			for box in self.boxes:
				x = 1 - (box[4] + box[2])/2/self.imsize[1]
				y = ((1 - (box[5] + box[3])/2/self.imsize[0])-0.5)*5
				
				if x < 0.5:
					self.player1.change_color(True)
					self.player1.center_y = max(0, min(self.height, int(y*self.height)))
				if x > 0.5:
					self.player2.change_color(True)
					#faceImg = cv2.resize(ret[0][box[3]:box[5],box[2]:box[4],:], (64,64))
					self.player2.center_y = max(0, min(self.height, int(y*self.height)))

class PongApp(App):
	def build(self):
		game = PongGame()
		game.serve_ball()
		Clock.schedule_interval(game.update, 1.0 / 60.0)
		return game


if __name__ == '__main__':
	PongApp().run()

