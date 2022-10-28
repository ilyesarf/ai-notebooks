from this import d
import pygame
pygame.init()
import math
import time

class Dot:
	def __init__(self):
		self.px: float
		self.py: float
		self.links = 0

class Link:
	def __init__(self):
		self.p1x: float
		self.p1y: float
		
		self.p2x: float
		self.p2y: float

		self.color = ""	


class Grid:
	def __init__(self):
		self.H = 800
		self.W = 800
		self.screen = pygame.display.set_mode((self.W, self.H)) 
		self.n, self.m = self.maxn_dots()
		self.generate_dots()

	### self.dots ###
	def maxn_dots(self):
		self.space = 70

		n = (self.H-(30*2))//self.space #max self.dots in a column
		if self.H != self.W:
			m = (self.W-(30*2))//self.space #max self.dots in a row
			return n, m #rectangle n != m

		return n, n #square, n = m
	
	def neighboring_dots(self, dot): #max self.links per dot
		neighbors = 0

		all_pos = []
		for col in range(len(self.dots)):
			for d in self.dots[col]:
				all_pos.append((d.px, d.py))
		
		for pos in [(dot.px+self.space, dot.py), (dot.px-self.space, dot.py), (dot.px, dot.py+self.space), (dot.px, dot.py-self.space)]:
			if pos in all_pos:
				neighbors += 1
		
		return neighbors	 
		
	def generate_dots(self):
		self.dots = []
		
		for i in range(self.n+1):
			col = []
			for row in range(self.m+1):
				dot = Dot()

				dot.px = 30+(self.space*row)
				dot.py = 30+(self.space*i)
				col.append(dot)
			self.dots.append(col)


	def click_dot(self):
		mouse_pos = pygame.mouse.get_pos()

		for row in range(len(self.dots)): #check in which row the user clicked			

			py = self.dots[row][0].py #the same px in the whole column

			if mouse_pos[1] in range(py-self.radius, py+self.radius+1):
				for dot in self.dots[row]:
					sqr_x = (mouse_pos[0] - dot.px)**2
					sqr_y = (mouse_pos[1] - dot.py)**2

					if math.sqrt(sqr_x + sqr_y) < self.radius: #click in circle
						return dot
					else:
						pass
			
			else:
				pass

	def draw_dots(self):
		self.radius = 10

		for col in self.dots:
			for dot in col:					
				pygame.draw.circle(self.screen, pygame.color.Color('red' if dot.links > 0 else 'green'), (dot.px, dot.py), self.radius)
		
		if len(self.links) > 0: 
			for link in self.links:
				pygame.draw.line(self.screen, link.color, (link.p1x, link.p1y), (link.p2x, link.p2y))

	### LINKS ###
	def maxn_links(self):
		if self.n != self.m:
			return self.n*(self.m-1)+self.m*(self.n-1)
		
		return 2*(self.n**2-self.n)		

	def create_link(self, dot1, dot2, color):
		link = Link()
		link.color = color

		if dot1.py == dot2.py: #same column, horizontal link
			if dot1.px < dot2.px:
				link.p1x, link.p1y = dot1.px+self.radius, dot1.py
				link.p2x, link.p2y = dot2.px-self.radius, dot2.py
			else:
				link.p1x, link.p1y = dot1.px-self.radius, dot1.py
				link.p2x, link.p2y = dot2.px+self.radius, dot2.py
		

		elif dot1.px == dot2.px: #same row, vertical link
			if dot1.py < dot2.py:
				link.p1x, link.p1y = dot1.px, dot1.py+self.radius
				link.p2x, link.p2y = dot2.px, dot2.py-self.radius
			else:
				link.p1x, link.p1y = dot1.px, dot1.py-self.radius
				link.p2x, link.p2y = dot2.px, dot2.py+self.radius
		
		return link
	
	def link_dots(self):
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				dot = self.click_dot()
				color = 'white'

				if dot:
					print(id(dot))
					if self.clicked_dot and (self.clicked_dot.px, self.clicked_dot.py) in [(dot.px+self.space, dot.py), (dot.px-self.space, dot.py), (dot.px, dot.py+self.space), (dot.px, dot.py-self.space)]: #check if clicked_dot is near dot
						link = self.create_link(self.clicked_dot, dot, color)
						self.links.append(link)

						dot.links += 1
						
						for col in self.dots:
							for index, item in enumerate(col):
								if id(item) == id(self.clicked_dot):
									col[index].links += 1

						self.clicked_dot = None

					elif dot.links < self.neighboring_dots(dot):
						self.clicked_dot = dot
				else:
					self.clicked_dot = None

	def generate_grid(self):
		self.links = []

		pygame.display.set_caption('Gridding')
		
		self.draw_dots()
		
		running = True
		self.clicked_dot = None
		while running:
			if pygame.event.get(pygame.QUIT): break

			self.screen.fill("black")
			
			self.link_dots()
		

			self.draw_dots()
		
			pygame.display.flip()	

			
			
	
if __name__ == '__main__':
	Grid().generate_grid()


