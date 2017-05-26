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
import winsound
from threading import *
from tkinter.font import Font

_bangSmall = "sounds/bangSmall.wav"
_bangMedium = "sounds/bangMedium.wav"
_bangLarge = "sounds/bangLarge.wav"
_fire = "sounds/fire.wav"
_rotationValues = { "Left": 1, "Right": -1 }
_asteroidTypes = {
	"big": [0, 14, 6, 31, 1, 60, 16, 64, 26, 78, 63, 73, 77, 46, 72, 24, 77, 8, 55, 0, 35, 5, 23, 0],
	"medium": [12, 0, 0, 4, 7, 14, 0, 19, 0, 32, 10, 38, 31, 35, 37, 30, 32, 25, 38, 18, 35, 2],
	"small": [1, 1, 4, 8, 1, 12, 9, 18, 17, 13, 17, 4, 10, 0]
 }
_frameRate = 20
_acc_rate = 0.1
_max_max = 4
_shipCoordinates = [200, 189, 193, 211, 197, 207, 203, 207, 207, 211]
_flameCoordinates = [ 198, 207, 200, 212, 202, 207, 198, 207 ]
		
class Board():
	gameState = None
	bulletList = []
	explosionList = []
	asteroidList = []
	debrisList = []
	
	def __init__( self, coordinates, outline, fill, tag, state ):	
		self.coordinates = coordinates
		self.outline = outline
		self.fill = fill
		self.tag = tag
		self.state = state
	
	def get_asteroid_by_id(id):
		for asteroid in Board.asteroidList:
			if asteroid.reference == id:
				return asteroid

	def generate_asteroids(num=2, offsetX=0, offsetY=0, size="big"):
		for i in range(num):
			Board.asteroidList.append(
				Asteroid(
					coordinates=Board.set_asteroid_coords(size, offsetX, offsetY), 
					direction=random.uniform(0, 2 * math.pi), 
					size=size
					)
				)
			
	def set_asteroid_coords( type, offsetX=0, offsetY=0):
		coords = []
		
		for coord1, coord2 in zip(_asteroidTypes[type][0::2], _asteroidTypes[type][1::2]):
			coords.extend([coord1 + random.uniform(0, 10) + offsetX, coord2 + random.uniform(0, 10) + offsetY])
		
		if not offsetX and not offsetY:
			loop = True
			
			while ( loop ):
				loop = False
				
				offsetX = random.uniform(0, 400)
				offsetY = random.uniform(0, 400)
				
				for item in Board.canvas.find_overlapping( 
							offsetX -min(coords[0::2]) -100, 
							offsetY -min(coords[1::2]) -100, 
							offsetX +max(coords[0::2]) +100, 
							offsetY +max(coords[1::2]) +100
					):
						if Board.canvas.gettags(item) and Board.canvas.gettags(item)[0] == 'ship':
							loop = True
							break
				if loop:
					continue
				
				coords[0::2] = [x + offsetX for x in coords[0::2]]
				coords[1::2] = [y + offsetY for y in coords[1::2]]
			
		return coords
		
	def get_center(self):
		x_center = 0
		y_center = 0
		
		for coord1, coord2 in zip( Board.canvas.coords(self.reference)[0::2], Board.canvas.coords(self.reference)[1::2] ):
			x_center += coord1
			y_center += coord2
		
		x_center /= (len(Board.canvas.coords(self.reference)) / 2 )
		y_center /= (len(Board.canvas.coords(self.reference)) / 2 )

		return x_center, y_center

	def outbound_reset(self):
		x_center, y_center = self.get_center()
		
		new_coords = []
		
		_x = 0
		_y = 0
		
		if (x_center < 0): _x = 400
		elif (x_center > 400): _x  = -400
		
		if (y_center < 0): _y = 400
		elif (y_center > 400): _y = -400

		for coord1, coord2 in zip(Board.canvas.coords(self.reference)[0::2], Board.canvas.coords(self.reference)[1::2]):
			new_coords.extend([coord1+_x, coord2+_y])
		Board.canvas.coords(self.reference, new_coords)

class Bullet(Board):
	def __init__(
		self,
		coordinates, 
		direction,
		outline="white", 
		fill="", 
		tag="bullet",
		state=NORMAL
		):
		
		super().__init__(coordinates, outline, fill, tag, state)
		self.dx = math.cos(direction) * 10
		self.dy = math.sin(direction) * 10
		
		self.reference = Board.canvas.create_oval( self.coordinates, outline=self.outline, fill=self.fill, tag=self.tag, state=self.state )

class Asteroid(Board):
	def __init__(
		self,
		coordinates, 
		direction,
		outline="white", 
		fill="", 
		size="big",
		tag="asteroid",
		state=NORMAL
		):
		
		super().__init__(coordinates, outline, fill, tag, state)
		self.size = size
		
		if size == "big": _speed = 1
		elif size == "medium": _speed = 2
		elif size == "small": _speed = 3
		
		self.dx = math.cos(direction) * _speed
		self.dy = math.sin(direction) * _speed
		
		self.reference = Board.canvas.create_polygon( self.coordinates, outline=self.outline, fill=self.fill, tag=self.tag, state=self.state )
	
	def destroy(self):	
		for x in range(-2, len(Board.canvas.coords(self.reference)) - 2, 2 ):
			self.debrisList.append(
				Debris(
					coordinates=[
						Board.canvas.coords(self.reference)[x],
						Board.canvas.coords(self.reference)[x+1],
						Board.canvas.coords(self.reference)[x+2],
						Board.canvas.coords(self.reference)[x+3]
					], direction=random.uniform(0, 2 * math.pi)
				)
			)
		
		if self.size == "big":
			Board.score+=100
			winsound.PlaySound(_bangLarge, winsound.SND_ALIAS|winsound.SND_ASYNC|winsound.SND_NOWAIT)
			Board.generate_asteroids(2, Board.canvas.coords(self.reference)[0], Board.canvas.coords(self.reference)[1], "medium")

		elif self.size == "medium":
			Board.score+=200
			winsound.PlaySound(_bangMedium, winsound.SND_ALIAS|winsound.SND_ASYNC|winsound.SND_NOWAIT)
			
			Board.generate_asteroids(2, Board.canvas.coords(self.reference)[0], Board.canvas.coords(self.reference)[1], "small")
		elif self.size == "small":
			Board.score+=300
			winsound.PlaySound(_bangSmall, winsound.SND_ALIAS|winsound.SND_ASYNC|winsound.SND_NOWAIT)
		
		Board.asteroidList.remove(self)
		
class Ship(Board):
	exist = False
	def __init__(
		self,
		coordinates=_shipCoordinates, 
		outline="white", 
		fill="", 
		tag="ship",
		state=NORMAL
		):
		
		Ship.exist = True
		super().__init__(coordinates, outline, fill, tag, state)
		
		self.face = -math.pi / 2
		self.dx = 0
		self.dy = 0
		
		self.reference = Board.canvas.create_polygon( self.coordinates, outline=self.outline, fill=self.fill, tag=self.tag, state=self.state )
		self.acc = False
		self.rot = False
		self.rotationDir = None
		
		self.flame = Flame()	

	def outbound_reset(self):
		x_center, y_center = self.get_center()
		
		new_ship_coords = []
		new_flame_coords = []
		
		_x = 0
		_y = 0
		
		if (x_center < 0): _x = 400
		elif (x_center > 400): _x  = -400
		
		if (y_center < 0): _y = 400
		elif (y_center > 400): _y = -400

		for coord1, coord2 in zip(Board.canvas.coords(self.reference)[0::2], Board.canvas.coords(self.reference)[1::2]):
			new_ship_coords.extend([coord1+_x, coord2+_y])
		Board.canvas.coords(self.reference, new_ship_coords)
		
		for coord1, coord2 in zip(Board.canvas.coords(self.flame.reference)[0::2], Board.canvas.coords(self.flame.reference)[1::2]):
			new_flame_coords.extend([coord1+_x, coord2+_y])
		Board.canvas.coords(self.flame.reference, new_flame_coords)
		
	def acc_on(self):
		if not self.acc:
			self.acc = True
			Board.canvas.itemconfig(self.flame.reference, state=NORMAL)
	def acc_off(self):
		self.acc = False
		Board.canvas.itemconfig(self.flame.reference, state=HIDDEN)
		
	def rot_on(self):
		if not self.rot: self.rot = True
	def rot_off(self):
		self.rot = False
	
	def rotate(self, direction):
		t = math.pi / 180 * 5 * _rotationValues[direction]
		
		self.face -= t
		
		def _rot(x, y):
			x -= x_center
			y -= y_center
			_x = x * math.cos(t) + y * math.sin(t)
			_y = -x * math.sin(t) + y * math.cos(t)
			return _x + x_center, _y + y_center

		new_ship_coords = []
		new_flame_coords = []
		x_center, y_center = self.get_center()
		
		for coord1, coord2 in zip(Board.canvas.coords(self.reference )[0::2], Board.canvas.coords(self.reference)[1::2]):
			new_ship_coords.extend(_rot(coord1, coord2))
		
		for coord1, coord2 in zip(Board.canvas.coords(self.flame.reference)[0::2], Board.canvas.coords(self.flame.reference)[1::2]):
			new_flame_coords.extend(_rot(coord1, coord2))
			
		Board.canvas.coords(self.reference, new_ship_coords)
		Board.canvas.coords(self.flame.reference, new_flame_coords)
	
	def destroy(self):
		x_center, y_center = self.get_center()
		
		Board.explosionList.append(
			Explosion(
				coordinates=[
					x_center - 5,
					y_center - 5,
					x_center + 5,
					y_center + 5
				]
			)		
		)	
		
		for x in range(-2, len(Board.canvas.coords(self.reference)) - 2, 2 ):
			self.debrisList.append(
				Debris(
					coordinates=[
						Board.canvas.coords(self.reference)[x],
						Board.canvas.coords(self.reference)[x+1],
						Board.canvas.coords(self.reference)[x+2],
						Board.canvas.coords(self.reference)[x+3]
					], direction=random.uniform(0, 2 * math.pi)
				)
			)			
		Board.canvas.delete(self.flame.reference)
		Board.canvas.delete(self.reference)
		winsound.PlaySound(_bangSmall, winsound.SND_ALIAS|winsound.SND_ASYNC|winsound.SND_NOWAIT)		
	
class Flame(Board):
	exist = False
	def __init__(
		self, 
		coordinates=_flameCoordinates, 
		outline="white", 
		fill="", 
		tag="flame", 
		state=HIDDEN
		):
		
		super().__init__(coordinates, outline, fill, tag, state)
		
		self.reference = Board.canvas.create_polygon( self.coordinates, outline=self.outline, fill=self.fill, tag=self.tag, state=self.state )

class Debris(Board):		
	def __init__(
		self, 
		coordinates, 
		direction,
		outline="white", 
		fill="", 
		tag="debris", 
		state=NORMAL
		):
		
		self.dx = math.cos(direction) * random.uniform(0,2)
		self.dy = math.sin(direction) * random.uniform(0,2)
		self.timer = random.uniform(20, 255)
		
		super().__init__(coordinates, outline, fill, tag, state)
		self.reference = Board.canvas.create_line( self.coordinates, fill=self.outline, tag=self.tag, state=self.state )
	
	def destroy(self):
		Board.canvas.delete(self.reference)	
		Board.debrisList.remove(self)

class Explosion(Board):		
	def __init__(
		self, 
		coordinates, 
		outline="white", 
		fill="", 
		tag="explosion", 
		state=NORMAL
		):
		
		self.timer = random.uniform(200, 255)
		
		super().__init__(coordinates, outline, fill, tag, state)
		self.reference = Board.canvas.create_oval( self.coordinates, outline=self.outline, fill=self.fill, tag=self.tag, state=self.state )
	
	def destroy(self):
		Board.canvas.delete(self.reference)	
		Board.explosionList.remove(self)
		
class game_controller(object):
	def next_level(self):
		self.currentAsteroidNum += 1
		Thread(target=Board.generate_asteroids(self.currentAsteroidNum) ).start()
		self.nextLevelBool = True

	def set_respawn(self):
		self.respawn = True
	
	def moveit(self):
		for explosion in Board.explosionList:
			if explosion.timer < 0:
				explosion.destroy()
			else:
			
				if explosion.timer <= 16:
					color = "#" + '0{0:x}'.format(int(explosion.timer))*3
				else:
					color = "#" + '{0:x}'.format(int(explosion.timer))*3
				
				Board.canvas.itemconfig(explosion.reference, outline=color)
				
				Board.canvas.coords(explosion.reference, 
					[
						Board.canvas.coords(explosion.reference)[0] - 1,
						Board.canvas.coords(explosion.reference)[1] - 1,
						Board.canvas.coords(explosion.reference)[2] + 1,
						Board.canvas.coords(explosion.reference)[3] + 1,
					]
				)
				
				explosion.timer -= random.uniform(0,10)
	
		for debris in Board.debrisList:
			if debris.timer < 0:
				debris.destroy()
			else:
				Board.canvas.itemconfig(debris.reference, fill="#" + '{0:x}'.format(int(debris.timer))*3)
				Board.canvas.move(debris.reference, debris.dx, debris.dy )
				debris.timer -= random.uniform(0,3)
		
		if self.respawn:
			loop = False
		
			for item in Board.canvas.find_overlapping( 
				min(_shipCoordinates[0::2]) -50, 
				min(_shipCoordinates[1::2]) -50, 
				max(_shipCoordinates[0::2]) +50, 
				max(_shipCoordinates[1::2]) +50
			):
				if Board.canvas.gettags(item) and Board.canvas.gettags(item)[0] == 'asteroid':
					loop = True
					break
			
			if not loop:
				self.respawn = False
				self.ship = Ship()
				self.shot = False
			
		if not Board.asteroidList and self.nextLevelBool:
			self.nextLevelBool = False
			Timer(3, self.next_level ).start()
			
		for bullet in Board.bulletList:
			if Board.canvas.coords(bullet.reference)[0] < 0 or Board.canvas.coords(bullet.reference)[2] > 400 or Board.canvas.coords(bullet.reference)[1] < 0 or Board.canvas.coords(bullet.reference)[3] > 400:
				Board.canvas.delete(bullet.reference)
				Board.bulletList.remove(bullet)
				continue
			else:
				for item in Board.canvas.find_overlapping( Board.canvas.coords(bullet.reference)[0], Board.canvas.coords(bullet.reference)[1], Board.canvas.coords(bullet.reference)[2], Board.canvas.coords(bullet.reference)[3], ):
					if Board.canvas.gettags(item)[0] == 'bullet' or Board.canvas.gettags(item)[0] == 'ship':
						continue
					elif Board.canvas.gettags(item)[0] == 'asteroid':
						asteroid = Board.get_asteroid_by_id(item)
						
						x_center, y_center = bullet.get_center()
						
						Board.explosionList.append(
							Explosion(
								coordinates=[
									x_center - 5,
									y_center - 5,
									x_center + 5,
									y_center + 5
								]
							)		
						)
						
						asteroid.destroy()
						
						Board.canvas.delete(bullet.reference)
						Board.bulletList.remove(bullet)
						Board.canvas.delete(item)
						
						self.scoreLabel.config(text="Score: {}".format(Board.score))
						break

				Board.canvas.move(bullet.reference, bullet.dx, bullet.dy)	

		for asteroid in Board.asteroidList:
			for item in Board.canvas.find_overlapping(	min(Board.canvas.coords(asteroid.reference)[0::2]) + 5, min(Board.canvas.coords(asteroid.reference)[1::2]) + 5, max(Board.canvas.coords(asteroid.reference)[0::2]) - 5, max(Board.canvas.coords(asteroid.reference)[1::2]) - 5):
				if Board.canvas.gettags(item) and Board.canvas.gettags(item)[0] == 'ship':
					if hasattr(self, 'ship'):
						self.ship.destroy()
						Ship.exist = False 
						
						if self.currentLives >= 1:
							self.currentLives -= 1
							Board.canvas.itemconfig(self.lifeCounter, text=self.currentLives)
							
							Timer(3, self.set_respawn ).start()
						else:
							Board.canvas.itemconfig(self.title, state=NORMAL, text="Game over")
							Board.canvas.itemconfig(self.instructions, state=NORMAL, text="Press Enter to play again")
					
			asteroid.outbound_reset()
			
			Board.canvas.move(asteroid.reference, asteroid.dx, asteroid.dy)
	
		if Ship.exist:
			if self.ship.acc:
				if self.ship.dx + _acc_rate * math.cos(self.ship.face) < _max_max and self.ship.dx + _acc_rate * math.cos(self.ship.face) > -_max_max:
					self.ship.dx += _acc_rate * math.cos(self.ship.face) 
				
				if self.ship.dy + _acc_rate * math.sin(self.ship.face) < _max_max and self.ship.dy + _acc_rate * math.sin(self.ship.face) > -_max_max:
					self.ship.dy += _acc_rate * math.sin(self.ship.face) 
					
			if self.ship.rot:
				self.ship.rotate(self.ship.rotationDir)
			self.ship.outbound_reset()
			
		Board.canvas.move(self.ship.reference, self.ship.dx,  self.ship.dy )
		Board.canvas.move(self.ship.flame.reference, self.ship.dx, self.ship.dy )
	
		if Board.gameState == True:
			self.root.after(_frameRate, self.moveit)
		elif Board.gameState == False:
			Board.gameState = None
			self.new_game()		

	def	shoot(self, event=None):
		if Ship.exist:
			if self.shot:
				pass
			else:
				winsound.PlaySound(_fire, winsound.SND_ALIAS|winsound.SND_ASYNC|winsound.SND_NOWAIT)
				Board.bulletList.append(
					Bullet(
						[
							Board.canvas.coords(self.ship.reference)[0]-1, 
							Board.canvas.coords(self.ship.reference)[1]-1, 
							Board.canvas.coords(self.ship.reference)[0]+1, 
							Board.canvas.coords(self.ship.reference)[1]+1
						], self.ship.face)
					)
				self.shot = True
				
	def release(self, event=None):
		self.shot = False
	
	def	rotate(self, event=None):
		if Ship.exist:
			self.ship.rotationDir = event.keysym
			self.ship.rot_on()
	def	unrotate(self, event=None):
		self.rotationDir = None
		self.ship.rot_off()
		
	def on(self, event=None):
		if Ship.exist:
			self.ship.acc_on()
	def off(self, event=None):
		if Ship.exist:
			self.ship.acc_off()

	def create_menu(self):
		self.score = 0
		
		self.divLine = Board.canvas.create_line(450, 0, 450, 400, fill="white")
		self.liveVar = IntVar() 
		self.liveVar.set(5)
		
		self.asteroidNumVar = StringVar()
		self.asteroidNumVar.set("Medium")
		
		self.scoreLabel = Label(Board.canvas, text="Score: {}".format(self.score), bg="black", fg="white")
		self.scoreLabel.place(x=460,y=50)
		
		self.liveLabel = Label(Board.canvas, text="Init lives:", bg="black", fg="white")
		self.liveLabel.place(x=460,y=120)
		self.liveOption = OptionMenu(Board.canvas, self.liveVar, 1,2,3,4,5,6,7,8,9,10)
		self.liveOption.place(x=460,y=140)
		
		self.button1 = Button(Board.canvas, text = "New game", anchor = W, command = self.new_game, bg="black", fg="white")
		self.button1.place(x=460,y=25)
		self.button2 = Button(Board.canvas, text = "Quit", anchor = W, command = self.quit, bg="black", fg="white")
		self.button2.place(x=530,y=25)	
		
		self.asteroidNumLabel = Label(Board.canvas, text="Init Asteroid Number:", bg="black", fg="white")
		self.asteroidNumLabel.place(x=460,y=180)
		self.asteroidNumOption = OptionMenu(Board.canvas, self.asteroidNumVar, "Random", "Low", "Medium", "High")
		self.asteroidNumOption.place(x=460,y=200)			
	
	def new_game(self):
		if Board.gameState == None:
			for bullet in Board.bulletList:
				Board.canvas.delete(bullet.reference)			
			for asteroid in Board.asteroidList:
				Board.canvas.delete(asteroid.reference)					

			Board.asteroidList = []
			Board.bulletList = []
			
			if Ship.exist:
				Board.canvas.delete(self.ship.reference)
			
			Board.score = 0
			self.nextLevelBool = True
			self.respawn = False
			self.scoreLabel.config(text="Score: {}".format(Board.score))
			
			self.currentLives = self.liveVar.get()
			self.ship = Ship()
			self.shot = False
			
			self.currentAsteroidNumVar = self.asteroidNumVar.get()
			if self.currentAsteroidNumVar == "Random":
				self.currentAsteroidNum = random.choice(range(2,7))
				Board.generate_asteroids(self.currentAsteroidNum)
			elif self.currentAsteroidNumVar == "Low":
				self.currentAsteroidNum = 2
				Board.generate_asteroids(self.currentAsteroidNum)
			elif self.currentAsteroidNumVar == "Medium":
				self.currentAsteroidNum = 4
				Board.generate_asteroids(self.currentAsteroidNum)
			elif self.currentAsteroidNumVar == "High":
				self.currentAsteroidNum = 6
				Board.generate_asteroids(self.currentAsteroidNum)
			
			Board.canvas.itemconfig(self.title, state=HIDDEN)
			Board.canvas.itemconfig(self.instructions, state=HIDDEN)
			
			Board.canvas.itemconfig(self.lifeCounterIcon, state=NORMAL)
			Board.canvas.itemconfig(self.lifeCounter, state=NORMAL, text=self.currentLives)
			
			Board.gameState = True		
			self.root.after(_frameRate, self.moveit)
		elif Board.gameState == False:
			pass
		elif Board.gameState:
			Board.gameState = False
			
# 	Quit game		
	def quit(self):
		self.root.destroy()	
		
# 	Setup control bindings
	def set_controls(self):
		self.root.bind('<Left>', self.rotate)
		self.root.bind('<Right>', self.rotate)
		
		self.root.bind('<KeyRelease-Left>', self.unrotate)
		self.root.bind('<KeyRelease-Right>', self.unrotate)
		
		self.root.bind('<Up>', self.on)
		self.root.bind('<KeyRelease-Up>', self.off)
		self.root.bind('<space>', self.shoot)
		self.root.bind('<KeyRelease-space>', self.release)	

#	Initialize main game object		
	def __init__(self, root):
		self.root = root
		Board.canvas = Canvas(root, width=600, height=400, bg="black")
		Board.canvas.pack()
		
		self.title = Board.canvas.create_text(230, 100, text="Asteroids Tk", font=Font(family="Alien Encounters", size=40), fill="white", tag="title")
		self.instructions = Board.canvas.create_text(230, 300, text="Press Enter to start", font=Font(family="Alien Encounters", size=15), fill="white", tag="instructions")
		self.lifeCounterIcon = Board.canvas.create_polygon( [28.0, 19.0, 21.0, 41.0, 25.0, 37.0, 31.0, 37.0, 35.0, 41.0], outline="white", fill="", tag="lifeCounterIcon", state=HIDDEN )
		self.lifeCounter = Board.canvas.create_text(55, 30, text="0", font=Font(family="Alien Encounters", size=20), fill="white", tag="instructions", state=HIDDEN)
		
#		Board.canvas.move(self.lifeCounterIcon, 10, 0)
		
#		print( Board.canvas.coords(self.lifeCounterIcon) )
		
		self.set_controls()
		self.create_menu()
		
if __name__ == "__main__":
	root = Tk()
	root.title("Asteroids Tk")
	game = game_controller(root);
	root.mainloop()
