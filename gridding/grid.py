import pygame
pygame.init()

class Dot:
    def __init__(self):
        self.px: float
        self.py: float
        self.connections: list


class Grid:
    def __init__(self):
        self.H = 800
        self.W = 1000
        self.screen = pygame.display.set_mode((self.W, self.H)) 
        self.n, self.m = self.maxn_dots()

    def maxn_dots(self):
        self.space = 70
        
        n = (self.H-(30*2))//self.space #max dots in a column
        if self.H != self.W:
            m = (self.W-(30*2))//self.space #max dots in a row
            return n, m #rectangle n != m
        
        return n, n #square, n = m
    
    def generate_dots(self):
        dots = []

        for col in range(self.n):
            for row in range(self.m):
                dot = Dot()
                    
                dot.px = 30+(self.space*row)
                dot.py = 30+(self.space*col)
                dots.append(dot)
        

        return dots


    def draw_dots(self):
        dots = self.generate_dots()
        radius = 10
        color = 'green'

        for dot in dots:
            pygame.draw.circle(self.screen, color, (dot.px, dot.py), radius)       
    
    def generate_grid(self):
        pygame.display.set_caption('Gridding')
        
        self.draw_dots() 
        pygame.display.flip()
        pygame.display.update()
       
        running = True
        while running:
            self.screen.fill("black")
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            


Grid().generate_grid()


