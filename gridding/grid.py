#!/usr/bin/env python3
import pygame
pygame.init()
import math
import sys
import screeninfo

class Dot:
    def __init__(self):
        self.px: float
        self.py: float
        self.links = 0
        self.radius = 15

    def neighboring_dots(self, space, dots): #max links per dot
        neighbors = 0

        all_pos = []
        for col in range(len(dots)):
            for d in dots[col]:
                all_pos.append((d.px, d.py))
        
        for pos in [(self.px+space, self.py), (self.px-space, self.py), (self.px, self.py+space), (self.px, self.py-space)]:
            if pos in all_pos:
                neighbors += 1
        
        return neighbors

class Link:
    def __init__(self):
        self.p1x: float
        self.p1y: float
        
        self.p2x: float
        self.p2y: float

        self.player = 0 
    
class Grid:
    def __init__(self, n=None, m=None):
        self.players = 2
        self.link_colors = ['cyan', 'purple', 'yellow', 'white']
        self.monitor = screeninfo.get_monitors()[0]
        self.H = self.monitor.height-300
        self.W = self.monitor.width-300
        self.screen = pygame.display.set_mode((self.W, self.H))
        
        self.space = 75
        if not n and not m:
            self.n, self.m = self.maxn_dots()
        else:
            self.n, self.m = n, m

        self.possible_links = self.maxn_links()

        self.generate_dots()
    

    ### DOTS ###
    def maxn_dots(self):
        n = (self.H-(30*2))//self.space #max dots in a column
        if self.H != self.W:
            m = (self.W-(30*2))//self.space #max dots in a row
            return n, m #rectangle n != m

        return n, n #square, n = m   
        
    def generate_dots(self):
        self.dots = []
        
        for i in range(self.n):
            col = []
            for row in range(self.m):
                dot = Dot()

                dot.px = 30+(self.space*row)
                dot.py = 100+(self.space*i)
                col.append(dot)

            self.dots.append(col)


    def click_dot(self):
        radius = 15
        mouse_pos = pygame.mouse.get_pos()

        for row in range(len(self.dots)): #check in which row the user clicked          

            py = self.dots[row][0].py #the same px in the whole column

            if mouse_pos[1] in range(py-radius, py+radius+1):
                
                for dot in self.dots[row]:
                    sqr_x = (mouse_pos[0] - dot.px)**2
                    sqr_y = (mouse_pos[1] - dot.py)**2

                    if math.sqrt(sqr_x + sqr_y) < radius: #is click in circle
                        return dot
                    else:
                        pass
            
            else:
                pass


    def draw_dots(self):

        for col in self.dots:
            for dot in col:                 
                pygame.draw.circle(self.screen, pygame.color.Color('red' if dot.links > 0 else 'green'), (dot.px, dot.py), dot.radius)
        
        if len(self.links) > 0: 
            for link in self.links:
                pygame.draw.line(self.screen, self.link_colors[link.player], (link.p1x, link.p1y), (link.p2x, link.p2y))
    

    
    ### LINKS ###
    def maxn_links(self):
        if self.n != self.m:
            return 2*(self.n*(self.m-1)+self.m*(self.n-1))
        
        return 4*(self.n**2-self.n)     


    def create_link(self, dot1, dot2):
        link = Link()
        link.player = self.turn

        if dot1.py == dot2.py: #same column, horizontal link
            if dot1.px < dot2.px: #right to left
                right_dot = dot1
                left_dot = dot2 
            else: #reverse left to right
                right_dot = dot2
                left_dot = dot1
                
            link.p1x, link.p1y = right_dot.px+dot1.radius, dot1.py
            link.p2x, link.p2y = left_dot.px-dot2.radius, dot2.py
        

        elif dot1.px == dot2.px: #same row, vertical link
            if dot1.py < dot2.py: #up to down
                up_dot = dot1
                down_dot = dot2
                
            else: #down to up
                up_dot = dot2
                down_dot = dot1

            link.p1x, link.p1y = dot1.px, up_dot.py+up_dot.radius
            link.p2x, link.p2y = dot2.px, down_dot.py-down_dot.radius

        return link
    

    def link_exists(self, link):
        all_links_pos = [(link2.p1x, link2.p1y, link2.p2x, link2.p2y) for link2 in self.links]
        
        return (link.p1x, link.p1y, link.p2x, link.p2y) in all_links_pos


    def link_dots(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                dot = self.click_dot()

                if dot:
                    #check if clicked_dot is near dot
                    if self.clicked_dot and (self.clicked_dot.px, self.clicked_dot.py) in [(dot.px+self.space, dot.py), (dot.px-self.space, dot.py), (dot.px, dot.py+self.space), (dot.px, dot.py-self.space)]: 
                        
                        link = self.create_link(self.clicked_dot, dot)

                        if not self.link_exists(link):
                            
                            if link.p1y == link.p2y: #horizontal
                                print((link.p1x-dot.radius, link.p1y),(link.p2x+dot.radius, link.p2y))
                            elif link.p1x == link.p2x: #vertical
                                print((link.p1x, link.p1y-dot.radius), (link.p2x, link.p2y+dot.radius))
                            
                            
                            self.links.append(link)

                            for col in self.dots:
                                for index, item in enumerate(col):
                                    if id(item) == id(self.clicked_dot):
                                        col[index].links += 1
                                        
                            dot.links += 1
                            
                            if self.turn == 0:
                                self.turn = 1
                            else:
                                self.turn = 0

                            self.possible_links -= 2
                        
                        self.clicked_dot = None

                    elif dot.links < dot.neighboring_dots(self.space, self.dots):
                        self.clicked_dot = dot
                else:
                    self.clicked_dot = None
        
    
    
    ### SQUARES ###
    def is_square(self):
        pass
    
    def draw_square(self):
        pass


    ### OTHER ###
    def write_turn(self):
        font = pygame.font.Font('freesansbold.ttf', 40)
        text = font.render(f"It\'s {self.turn+1} player's turn", True, 'red')
        
        textRect = text.get_rect()
        textRect.center = (self.W // 2, 30)

        self.screen.blit(text, textRect)

    def generate_grid(self):
        self.links = []
        self.turn = 0

        pygame.display.set_caption('Gridding')
        
        
        self.clicked_dot = None

        while self.possible_links > 0:
            if pygame.event.get(pygame.QUIT): break

            self.screen.fill("black")
            self.write_turn()

            self.link_dots()
        
            self.draw_dots()
            
            pygame.display.flip()
        
        else:   
            print('Game ended')
            self.draw_dots()
            pygame.display.flip()
            pygame.time.delay(10*1000)
                
            """
            winners = self.get_winners()
            if winners > 1:
                print(f"It\'s a draw between {'&'.join([str(winner) for winner in winners])}")
            else:
                print(f'{winners[0]} won!!')
            """
                

            
#TODO: links or connected_dots?
    
if __name__ == '__main__':
    n, m = None, None
    if len(sys.argv) == 3:
        n, m = sys.argv[1:3]
    elif len(sys.argv) == 2:
        n = sys.argv[2]
        m = n
    
    Grid(int(n), int(m)).generate_grid()
