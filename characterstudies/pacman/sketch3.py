import pygame, sys, os, time, math
from pygame.locals import *

class Color:
	goofy_red = (255,100,100)
	dope_blue_darkness = (30, 45, 64)
	dope_blue_dark = (37, 52, 71)
	dope_blue_light = (40, 55, 74)
	electric_yellow = (249, 229, 38)


class Direction:
	forward = True
	backward = False

class Speed:
	high = 1
	med = 2
	low = 4


class PacMan:

	def __init__(self, position, dimensions):
		self.position = position
		self.dimensions = dimensions
		self.direction = Direction.forward
		self.color = Color.electric_yellow
		self.speed = Speed.high
		self.ticker = 1
		self.max_open_radians = 1.0
		self.current_open_radians = self.max_open_radians
		self.chomp_closing = True
		self.chomping = False

	def draw(self, surface):

		def half(x):
			return x/2
		left, top = self.position
		width, height = 100, 100
		center = (left + half(width), top + half(height))
		centerX, centerY = center

		start_radians = self.current_open_radians / 2.0
		end_radians = 2 * math.pi - start_radians
		
		# Direction will change things. If we're going backward we need to flip the pacman around.
		if self.direction == Direction.backward:
			start_radians = start_radians - math.pi
			end_radians = end_radians - math.pi

		radius = width / 2  # Assuming square!! Careful.
		mouth_x = radius * math.cos(start_radians)
		mouth_y = radius * math.sin(start_radians)
		# Assuming that our jaw opening is always symmetrical!

		rect = pygame.Rect(self.position, (width, height) )
		
		pygame.draw.arc(surface, self.color, rect, start_radians, end_radians, 3)
		pygame.draw.line(surface, self.color, center, (centerX + mouth_x, centerY - mouth_y), 3)
		pygame.draw.line(surface, self.color, center, (centerX + mouth_x, centerY + mouth_y), 3)

	def update(self):
		if self.ticker % self.speed == 0:
			self.ticker = 1 # reset

			motion = (-10, 10)[self.direction]

			self.position = (self.position[0] + motion, self.position[1])
			if self.direction == Direction.forward and self.position[0] > (self.dimensions[0] - 100):
				self.direction = Direction.backward
			elif self.position[0] <= 0:
				self.direction = Direction.forward

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

	pacmen = []

	pacmen.append(PacMan((0, 600), dimensions))
	pacmen.append(PacMan(initial_position, dimensions))
	pacmen.append(PacMan((0, 250), dimensions))
	pacmen.append(PacMan((500, 375), dimensions))


	pacmen[0].speed = Speed.med
	pacmen[0].colorize(Color.goofy_red)
	pacmen[0].chomping = True

	pacmen[1].max_open_radians = 1.0
	pacmen[1].chomping = True

	pacmen[2].speed = Speed.low
	pacmen[2].max_open_radians = 2.0

	pacmen[3].max_open_radians = 0.1


	while True:
		if QUIT in [event.type for event in pygame.event.get()]:
			break
		surface = pygame.display.get_surface()
		surface.fill(Color.dope_blue_dark)
		draw_grid(surface)

		for pacman in pacmen:
			pacman.update()
			pacman.draw(surface)

		pygame.display.flip()
		time.sleep(.001)


main()
