
import pygame, sys, os, time, math
from pygame.locals import *

class Color:
	goofy_red = (255,100,100)
	dope_blue_darkness = (30, 45, 64)
	dope_blue_dark = (37, 52, 71)
	dope_blue_light = (40, 55, 74)
	electric_yellow = (249, 229, 38)
	green = (0, 230, 50)
	dope_blue_ultralight = (140, 155, 174)


class Direction:
	right = 0.0
	left = math.pi
	up = math.pi / 2
	down = math.pi * 1.5
	x_axis = (left, right)
	y_axis = (up, down)

class Speed:
	zero = 0
	high = 1
	med = 2
	low = 4

class PacMan:

	def __init__(self, position, dimensions):
		self.left, self.top = position
		self.dimensions = dimensions
		self.direction = Direction.right
		self.color = Color.electric_yellow
		self.speed = Speed.high
		self.ticker = 1
		self.max_open_radians = 1.0
		self.current_open_radians = self.max_open_radians
		self.chomp_closing = True
		self.chomping = False
		self.orientation = Direction.right

	def draw(self, surface):

		width, height = 100, 100
		center = (self.left + width/2, self.top + height/2)
		centerX, centerY = center

		# half_open_arc is denoted as alpha in the notes.
		half_open_arc = self.current_open_radians / 2.0

		start_radians = self.orientation + half_open_arc
		end_radians = self.orientation - half_open_arc

		if end_radians < 0:
			end_radians = (math.pi * 2) + end_radians

		radius = width / 2  # Assuming our drawing rect is a square!! Careful.
		# Assuming that our jaw opening is always symmetrical!

		Sx = math.cos(start_radians) * radius
		Sy = math.sin(start_radians) * radius
		Ex = math.cos(end_radians) * radius
		Ey = math.sin(end_radians) * radius

		rect = pygame.Rect( (self.left, self.top), (width, height) )

		# Starting Ray
		pygame.draw.line(surface, self.color, center, (centerX + Sx, centerY - Sy), 3)

		# Ending Ray
		pygame.draw.line(surface, self.color, center, (centerX + Ex, centerY - Ey), 3)

		# Arc
		if (self.orientation - half_open_arc) <= 0:
			pygame.draw.arc(surface, self.color, rect, start_radians, math.pi, 3)
			pygame.draw.arc(surface, self.color, rect, math.pi, end_radians, 3)
		else:
			pygame.draw.arc(surface, self.color, rect, 0.0, end_radians, 3)
			pygame.draw.arc(surface, self.color, rect, start_radians, math.pi * 2, 3)

		# Add eyes
		if self.direction in Direction.x_axis:
			eyeball_offset = 25 * [-1, 1][self.direction == Direction.right]
			pygame.draw.circle(surface, self.color, (centerX + eyeball_offset, centerY - 35), 5)


	def work_mouth(self):
		if self.chomping:
			if self.chomp_closing:
				if self.current_open_radians > 0:
					self.current_open_radians -= 0.1
				else:
					self.chomp_closing = False
			else:
				if self.current_open_radians <= self.max_open_radians:
					self.current_open_radians += 0.1
				else:
					self.chomp_closing = True

	def update_position(self):
		motion = 10 if self.direction in (Direction.right, Direction.down) else -10


		if self.direction in Direction.x_axis:
			self.left = self.left + motion
			if self.direction == Direction.right and self.left > (self.dimensions[0] - 100):
				self.direction = Direction.left
			elif self.left <= 0:
				self.direction = Direction.right
		else:
			self.top = self.top + motion
			if self.direction == Direction.down and self.top > (self.dimensions[1] - 100):
				self.direction = Direction.up
			elif self.top <= 0:
				self.direction = Direction.down

		# Face the way we're moving.
		self.orientation = self.direction


	def update(self):
		if self.speed == Speed.zero: return
		if self.ticker % self.speed == 0:
			self.ticker = 1 # reset
			self.update_position()
			self.work_mouth()

		else:
			self.ticker += 1

	def colorize(self, color):
		self.color = color

	def set_speed(self, rate):
		# High, medium, or low. Determines how many updates we ignore.
		self._speed = rate

	def get_speed(self):
		return self._speed

	speed = property(get_speed, set_speed)


def draw_grid(surface):

	grid_size = 20

	for x in range(grid_size, surface.get_width(), grid_size):
		pygame.draw.line(surface, Color.dope_blue_light, (x, 0), (x, surface.get_height()), 1)

	for y in range(grid_size, surface.get_height(), grid_size):
		pygame.draw.line(surface, Color.dope_blue_light, (0, y), (surface.get_width(), y), 1)




def main():

	NAME = "GAME DEV, SKETCH 1"

	pygame.init()

	dimensions = (1024,800)

	window = pygame.display.set_mode(dimensions)

	pygame.display.set_caption(NAME)

	color = (100, 0, 150)
	modification = 0

	initial_position = (100, 100)

	pacman = PacMan((0, 600), dimensions)
	pacman.max_open_radians = 1.0
	pacman.chomping = True

	while True:
		if QUIT in [event.type for event in pygame.event.get()]:
			break
		surface = pygame.display.get_surface()
		surface.fill(Color.dope_blue_dark)
		draw_grid(surface)

		pacman.update()
		pacman.draw(surface)

		pygame.display.flip()
		time.sleep(.001)


main()
