#!/usr/bin/env python

__author__ = "Saulius Bartkus"
__copyright__ = "Copyright 2017"

__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Saulius Bartkus"
__email__ = "saulius181@yahoo.com"
__status__ = "Production"

from tkinter import *
import random
import math
import time

class game_controller(object):
	def moveit(self):
		for bullet in self.canvas.data["BulletList"]:
			if self.canvas.coords(bullet[0])[0] <0 or self.canvas.coords(bullet[0])[2] > 400 or self.canvas.coords(bullet[0])[1] < 0 or self.canvas.coords(bullet[0])[3] > 400:
				self.canvas.delete(bullet[0])
				self.canvas.data["BulletList"].remove(bullet)
				continue
			else:
				for item in self.canvas.find_overlapping( self.canvas.coords(bullet[0])[0], self.canvas.coords(bullet[0])[1], self.canvas.coords(bullet[0])[2], self.canvas.coords(bullet[0])[3], ):
					if self.canvas.gettags(item)[0] == 'bullet' or self.canvas.gettags(item)[0] == 'ship':
						continue
					elif self.canvas.gettags(item)[0] == 'asteroid':
						self.canvas.delete(bullet[0])
						self.canvas.data["BulletList"].remove(bullet)
						
						if self.canvas.gettags(item)[1] == "big":
						
							self.canvas.data["AsteroidList"].append(self.canvas.create_polygon( self.set_asteroid_coords("medium", self.canvas.coords(item)[0], self.canvas.coords(item)[1]), outline="white", fill="", tags="asteroid medium {} {}".format(math.cos(random.uniform(1, 10)) * 2, math.sin(random.uniform(1, 10)) * 2)))
							self.canvas.data["AsteroidList"].append(self.canvas.create_polygon( self.set_asteroid_coords("medium", self.canvas.coords(item)[0], self.canvas.coords(item)[1]), outline="white", fill="", tags="asteroid medium {} {}".format(math.cos(random.uniform(1, 10)) * 2, math.sin(random.uniform(1, 10)) * 2)))
						elif self.canvas.gettags(item)[1] == "medium":
							self.canvas.data["AsteroidList"].append(self.canvas.create_polygon( self.set_asteroid_coords("small", self.canvas.coords(item)[0], self.canvas.coords(item)[1]), outline="white", fill="", tags="asteroid small {} {}".format(math.cos(random.uniform(1, 10)) * 3, math.sin(random.uniform(1, 10)) * 3)))
							self.canvas.data["AsteroidList"].append(self.canvas.create_polygon( self.set_asteroid_coords("small", self.canvas.coords(item)[0], self.canvas.coords(item)[1]), outline="white", fill="", tags="asteroid small {} {}".format(math.cos(random.uniform(1, 10)) * 3, math.sin(random.uniform(1, 10)) * 3)))						
						
						self.canvas.delete(item)						
						self.canvas.data["AsteroidList"].remove(item)
						break
						
				self.canvas.move(bullet[0], bullet[1], bullet[2])

		for asteroid in self.canvas.data["AsteroidList"]:
			new_asteroid_coords = []
			x_center, y_center = self.get_center(asteroid)
			
			if (y_center < 0):
				for coord1, coord2 in zip(self.canvas.coords(asteroid)[0::2], self.canvas.coords(asteroid)[1::2]):
					new_asteroid_coords.extend([coord1, coord2+400])
				self.canvas.coords(asteroid, new_asteroid_coords)
				
			elif (y_center > 400):
				for coord1, coord2 in zip(self.canvas.coords(asteroid)[0::2], self.canvas.coords(asteroid)[1::2]):
					new_asteroid_coords.extend([coord1, coord2-400])
				self.canvas.coords(asteroid, new_asteroid_coords)
			
			new_asteroid_coords = []
			
			if (x_center < 0):
				for coord1, coord2 in zip(self.canvas.coords(asteroid)[0::2], self.canvas.coords(asteroid)[1::2]):
					new_asteroid_coords.extend([coord1+400, coord2])
				self.canvas.coords(asteroid, new_asteroid_coords)
				
			elif (x_center > 400):
				for coord1, coord2 in zip(self.canvas.coords(asteroid)[0::2], self.canvas.coords(asteroid)[1::2]):
					new_asteroid_coords.extend([coord1-400, coord2])
				self.canvas.coords(asteroid, new_asteroid_coords)
			
			self.canvas.move(asteroid, float(self.canvas.gettags(asteroid)[2]), float(self.canvas.gettags(asteroid)[3]))
			
		new_ship_coords = []
		new_flame_coords = []
		x_center, y_center = self.get_center(self.ship)
		
		if (y_center < 0):
			for coord1, coord2 in zip(self.canvas.coords(self.ship)[0::2], self.canvas.coords(self.ship)[1::2]):
				new_ship_coords.extend([coord1, coord2+400])
			self.canvas.coords(self.ship, new_ship_coords)
			
			for coord1, coord2 in zip(self.canvas.coords(self.flame)[0::2], self.canvas.coords(self.flame)[1::2]):
				new_flame_coords.extend([coord1, coord2+400])
			self.canvas.coords(self.flame, new_flame_coords)
			
		elif (y_center > 400):
			for coord1, coord2 in zip(self.canvas.coords(self.ship)[0::2], self.canvas.coords(self.ship)[1::2]):
				new_ship_coords.extend([coord1, coord2-400])
			self.canvas.coords(self.ship, new_ship_coords)
			
			for coord1, coord2 in zip(self.canvas.coords(self.flame)[0::2], self.canvas.coords(self.flame)[1::2]):
				new_flame_coords.extend([coord1, coord2-400])
			self.canvas.coords(self.flame, new_flame_coords)
			
		new_ship_coords = []
		new_flame_coords = []		
		if (x_center < 0):
			for coord1, coord2 in zip(self.canvas.coords(self.ship)[0::2], self.canvas.coords(self.ship)[1::2]):
				new_ship_coords.extend([coord1+400, coord2])
			self.canvas.coords(self.ship, new_ship_coords)
			
			for coord1, coord2 in zip(self.canvas.coords(self.flame)[0::2], self.canvas.coords(self.flame)[1::2]):
				new_flame_coords.extend([coord1+400, coord2])
			self.canvas.coords(self.flame, new_flame_coords)			
			
		elif (x_center > 400):
			for coord1, coord2 in zip(self.canvas.coords(self.ship)[0::2], self.canvas.coords(self.ship)[1::2]):
				new_ship_coords.extend([coord1-400, coord2])
			self.canvas.coords(self.ship, new_ship_coords)

			for coord1, coord2 in zip(self.canvas.coords(self.flame)[0::2], self.canvas.coords(self.flame)[1::2]):
				new_flame_coords.extend([coord1-400, coord2])
			self.canvas.coords(self.flame, new_flame_coords)
		
		
		self.canvas.move(self.ship, self.canvas.data["Speed"]["x"],  self.canvas.data["Speed"]["y"] )
		self.canvas.move(self.flame, self.canvas.data["Speed"]["x"],  self.canvas.data["Speed"]["y"] )
		
		self.root.after(20, self.moveit)
	
	def	any_key(self, event=None):
		print(event.keysym)
		
	def	shoot(self, event=None):
		if self.shot:
			pass
		else:
			self.canvas.data["BulletList"].append([self.canvas.create_oval(self.canvas.coords(self.ship)[0]-1, self.canvas.coords(self.ship)[1]-1, self.canvas.coords(self.ship)[0]+1, self.canvas.coords(self.ship)[1]+1, tag="bullet", outline="white"), math.cos(self.faceDir) * 10, math.sin(self.faceDir) * 10 ])
			self.shot = True
			
	def release(self, event=None):
		self.shot = False
	
	def get_center(self, item):
		x_center = 0
		y_center = 0
		
		for coord1, coord2 in zip(self.canvas.coords(item)[0::2], self.canvas.coords(item)[1::2]):
			x_center += coord1
			y_center += coord2
		
		x_center /= (len(self.canvas.coords(item)) / 2 )
		y_center /= (len(self.canvas.coords(item)) / 2 )

		return x_center, y_center
	
	def	rotate(self, event=None):
		t = math.pi / 180 * 5 * self.dirDict[event.keysym]
		
		self.faceDir -= t
		
		def _rot(x, y):
			x -= x_center
			y -= y_center
			_x = x * math.cos(t) + y * math.sin(t)
			_y = -x * math.sin(t) + y * math.cos(t)
			return _x + x_center, _y + y_center

		new_ship_coords = []
		new_flame_coords = []
		x_center, y_center = self.get_center(self.ship)
		
		for coord1, coord2 in zip(self.canvas.coords(self.ship)[0::2], self.canvas.coords(self.ship)[1::2]):
			new_ship_coords.extend(_rot(coord1, coord2))
		
		for coord1, coord2 in zip(self.canvas.coords(self.flame)[0::2], self.canvas.coords(self.flame)[1::2]):
			new_flame_coords.extend(_rot(coord1, coord2))
			
		self.canvas.coords(self.ship, new_ship_coords)
		self.canvas.coords(self.flame, new_flame_coords)
		
	def on(self, event=None):
		self.canvas.itemconfig(self.flame, state=NORMAL)
		if self.canvas.data["Speed"]["x"] + (math.cos(self.faceDir) * self.dirDict[event.keysym]) < 4 and self.canvas.data["Speed"]["x"] + (math.cos(self.faceDir) * self.dirDict[event.keysym]) > -4:
			self.canvas.data["Speed"]["x"] += math.cos(self.faceDir) * self.dirDict[event.keysym]
		if self.canvas.data["Speed"]["y"] + (math.sin(self.faceDir) * self.dirDict[event.keysym]) < 4 and self.canvas.data["Speed"]["y"] + (math.sin(self.faceDir) * self.dirDict[event.keysym]) > -4:
			self.canvas.data["Speed"]["y"] += math.sin(self.faceDir) * self.dirDict[event.keysym]
		
	def off(self, event=None):
		self.canvas.itemconfig(self.flame, state=HIDDEN)
	
	def set_asteroid_types(self):
		self.canvas.data["AsteroidTypes"]["big"] = [0, 14, 6, 31, 1, 60, 16, 64, 26, 78, 63, 73, 77, 46, 72, 24, 77, 8, 55, 0, 35, 5, 23, 0]
		self.canvas.data["AsteroidTypes"]["medium"] = [12, 0, 0, 4, 7, 14, 0, 19, 0, 32, 10, 38, 31, 35, 37, 30, 32, 25, 38, 18, 35, 2]
		self.canvas.data["AsteroidTypes"]["small"] = [1, 1, 4, 8, 1, 12, 9, 18, 17, 13, 17, 4, 10, 0]
		
	def set_asteroid_coords(self, type, offsetX=0, offsetY=0):
		coords = []
		if not offsetX:
			offsetX = random.uniform(0, 400)
		if not offsetY:
			offsetY = random.uniform(0, 400)
			
		for coord1, coord2 in zip(self.canvas.data["AsteroidTypes"][type][0::2], self.canvas.data["AsteroidTypes"][type][1::2]):
			coords.extend([coord1 + random.uniform(0, 10) + offsetX, coord2 + random.uniform(0, 10) + offsetY])
		
		return coords
			
	def generate_asteroids(self, num=5):
		for i in range(num):
			self.canvas.data["AsteroidList"].append(self.canvas.create_polygon( self.set_asteroid_coords("big"), outline="white", fill="", tags="asteroid big  {} {}".format(math.cos(random.uniform(1, 10)), math.sin(random.uniform(-5, 5)))))
	
	def __init__(self, root):
		self.root = root
		self.canvas = Canvas(root, width=400, height=400, bg="black")
		
		self.canvas.pack()
		
		self.root.bind('<Left>', self.rotate)
		self.root.bind('<Right>', self.rotate)
		self.root.bind('<Up>', self.on)
		
		self.root.bind('<KeyRelease-Up>', self.off)
		
		self.root.bind('<space>', self.shoot)
		self.root.bind('<KeyRelease-space>', self.release)
		
		self.ship = self.canvas.create_polygon( [200, 189, 193, 211, 197, 207, 203, 207, 207, 211], outline="white", fill="", tag="ship")
		self.flame = self.canvas.create_polygon( [198, 207, 200, 212, 202, 207, 198, 207], outline="white", fill="", tag="flame", state=HIDDEN)
		
		self.dirDict = {'Up':0.3, 'Down':-0.3, 'Left':2, 'Right':-2}
		self.faceDir = -math.pi / 2
		self.moveDir = -math.pi / 2
		self.shot = False
		
		self.canvas.data = { }
		self.canvas.data["BulletList"] = []
		self.canvas.data["AsteroidList"] = []
		self.canvas.data["AsteroidTypes"] = {}
		self.set_asteroid_types()
		self.generate_asteroids()
		
		self.canvas.data["Speed"] = {'x': 0, 'y':0}
		
		self.root.after(20, self.moveit)
		
if __name__ == "__main__":
	root = Tk()
	root.title("Asteroids Tk")
	game = game_controller(root);
	root.mainloop()
