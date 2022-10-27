import pygame
pygame.init()

class Dot:
    def __init__(self):
        self.px: float
        self.py: float
        self.connections: list


class Grid:
    def __init__(self):
        self.H = 1000
        self.W = 1000
        self.screen = pygame.display.set_mode((self.W, self.H)) 
        self.n, self.m = self.maxn_dots()

    def maxn_dots(self):
        self.space = 70
        
        n = (self.H-(30*2))//self.space #max dots in a column
        if self.H != self.W:
            m = (self.W-(30*2))//self.space #max dots in a row
            return n, m
        
        return n, 0
    
    def generate_dots(self):
        if self.m == 0:
            for count in self.n:
                dot = Dot()
                dot.px = 0

        pass


    def draw_dots(self):
        n, m = max_dots()
        if m == 0:
            for dot in range(n):
                pass

    def generate_grid(self):
        pygame.display.set_caption('Gridding')
        
        color = 'green'
        radius = 10
       
        for i in range(self.n):
            px = 30+(self.space*i)
            for j in range(self.n):
                py = 30+(self.space*j)
                pygame.draw.circle(self.screen, color, (px, py), radius)       
        
        pygame.display.flip()
        pygame.display.update()
       
        running = True
        while running:
            self.screen.fill("black")
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            


Grid().generate_grid()


