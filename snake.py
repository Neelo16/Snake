#!/usr/bin/env python

import pygame,random

class queue:
    def __init__(self):
        """Creates a queue - a sequence with a FIFO behaviour"""
        self.q = []
        
    def __repr__(self):        
        if self.q == []:
            return '< <'
        string = '< '
        for e in self.q:
            string += str(e) + ' < '
        return string
    
    def __iter__(self):
        return iter(self.q)
    
    def __contains__(self,e):
        return e in self.q
    
    def push(self,*els):
        """Adds given elements to the end of the queue"""
        for e in els:
            self.q += [e]
        
    def pop(self):
        """Removes and returns the first element from the queue"""
        if self.q == []:
            raise ValueError ('Can\'t pop from an empty queue')
        else:
            el = self.q[0]
            del(self.q[0])
            return el
        
    def first(self):
        """Returns the first element in the queue"""
        if self.q == []:
            raise ValueError ('Can\'t show first element of an empty queue')
        else:
            return self.q[0]
        
    
    def last(self):
        """Returns the last element in the queue"""
        if self.q == []:
            raise ValueError ('Can\'t show last element of an empty queue')        
        else:
            return self.q[-1]
    
    def el_list(self):
        """Returns a list with the elements in the queue"""
        return list(self.q)
    
class board:
    def __init__(self,size,dist=10):
        """Creates a board with given size (tuple in the form of (width,height),
        with positions having given distance between them. Default distance is
        10."""
        self.pos_val = {}
        y = 0
        x = 0
        self.pos_ini = (0,0)
        self.x = size[0]
        self.y = size[1]
        self.dist = dist
        self.pos_end = (self.x-dist,self.y-dist)
        for y in range(0,self.y,dist):
            for x in range(0,self.x,dist):
                self.pos_val[(x,y)] = 0
            
    def __repr__(self):
        string = ''
        for y in range(0,self.y,self.dist):
            for x in range(0,self.x,self.dist):
                string += str(self.pos_val[(x,y)])
            string += '\n'
        return string
            
    def start_pos(self):
        """Returns the starting point of the board (the closest point to the
        coordinate (0,0)"""
        return self.pos_ini
    
    def end_pos(self):
        """Returns the ending point of the board (the closest point to the
        coordinate (width,height)"""        
        return self.pos_end
    
    def width(self):
        """Returns the board's width"""
        return self.x
    
    def height(self):
        """Returns the board's height"""
        return self.y
            
    def fill_pos(self,pos,value=1):
        """Fills a position with a value. If no value is given, fills it with 
        1 """
        if pos in self.pos_val:
            self.pos_val[pos] = value
            
            
    def value_list(self,value=0):
        """Returns a list of positions that have value. If no value is given,
        returns empty positions (value = 0)"""
        lst = []
        for c in self.pos_val:
            if self.pos_val[c] == value:
                lst += [c]
        return lst
        

class snake:
    def __init__(self,pos,size=1,direc=(0,10)):
        """Creates a snake entity, with the given size and initial position
        on given pos, growing in the given direction. Default size is 1, default
        direction is down, with a default move distance of 10."""
        self.body = queue()
        self.direc = direc
        self.body.push(pos)
        for i in range(size-1):
            pos = sum_vec(pos,direc)
            self.body.push(pos)
        
    def move(self,pos,grow=False):
        """Moves the snake's body into a certain position. If grow is set to
        True, the body extends one position. Default value for grow is False."""
        self.body.push(pos)
        if not grow:
            return self.body.pop()
        
    def body_pos_list(self):
        """Returns a list with all the positions occupied by the snake's 
        body"""
        return self.body.el_list()
    
    def next_position(self):
        """Returns the next position that the snake will move to"""
        return sum_vec(self.direc,self.body.last())
    
    def show(self,screen):
        """Draws the snake on the given screen"""
        for e in self.body_pos_list():
            pygame.draw.rect(screen,(255,255,255),(e[0],e[1],10,10),0)
    
    def change_dir(self,direc):
        """Changes the snake's direction, unless it's turning to its death"""
        if sum_vec(self.body.last(),direc) not in self.body:
            self.direc = direc
    
class gameMenu:
    def __init__(self,screen,button_txt,bg_color,txt_color,title):
        self.buttons = []
        self.font = pygame.font.SysFont('arial',20)
        self.bg_color = bg_color        
        scr_width = screen.get_rect().width
        scr_height = screen.get_rect().height
        for text in button_txt:
            self.buttons.append(self.font.render(text,1,txt_color))
        num_buttons = len(self.buttons)
        for i,label in enumerate(self.buttons[::-1]):
            rect = label.get_rect()
            width = rect.width
            height = rect.height
            posx = scr_width/2 - width/2
            posy = (scr_height*5/8)-(4*(i)*height)
            self.buttons[i] = button(button_txt[i],label,(width,height),(posx,posy))
        self.title_font = pygame.font.SysFont('arial',30)
        title_label = self.title_font.render(title,1,txt_color)
        width = title_label.get_rect().width
        height = title_label.get_rect().height
        posx = scr_width/2 - width/2
        posy = (scr_height*5/8)-(2.8*num_buttons)*height
        self.title = button(title,title_label,(width,height),(posx,posy))
            
    def show(self,screen):
        for button in self.buttons:
            screen.blit(button.label,button.coord)
        screen.blit(self.title.label,self.title.coord)
        
class button:
    def __init__(self,name,label,size,coord):
        self.name = name
        self.label = label
        self.size = size
        self.coord = coord
        self.width = size[0]
        self.height = size[1]
        self.posx = coord[0]
        self.posy = coord[1]
        
def sum_vec(v1,v2):
    """Sums two vectors"""
    return (v1[0]+v2[0],v1[1]+v2[1])

        
def game():
    """Main game function"""
    size = (800,600)
    quit = False
    fullscreen = False
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Snake? Snake? SNAAAAAAAAKE')
    up = (0,-10)
    down = (0,10)
    left = (-10,0)
    right = (10,0)
    while not quit:
        gameOver = False
        area = board(size)
        snake_pos = random.choice(area.value_list())
        player = snake(snake_pos)    
        for pos in player.body_pos_list():
            area.fill_pos(pos)       
        while not gameOver and not quit:
            screen.fill((0,0,0))
            if area.value_list(2) == []:
                fruit = random.choice(area.value_list())
                area.fill_pos(fruit,2)                
            pygame.draw.rect(screen,(40,150,10),(fruit[0],fruit[1],10,10),0)
            player.show(screen)
            pygame.display.flip()
            clock.tick(60)
            next_pos = player.next_position()
            #player.body.push(next_pos)  # Uncomment this for a funny experience
            if next_pos in area.value_list(1):
                gameOver = True
                break
            if next_pos[0] > area.end_pos()[0]:
                next_pos = (area.start_pos()[0],next_pos[1])
            elif next_pos[0] < area.start_pos()[0]:
                next_pos = (area.end_pos()[0],next_pos[1])            
            if next_pos[1] > area.end_pos()[1]:
                next_pos = (next_pos[0],area.start_pos()[1])
            elif next_pos[1] < area.start_pos()[1]:
                next_pos = (next_pos[0],area.end_pos()[1])
            area.fill_pos(next_pos,1)
            area.fill_pos(player.move(next_pos,fruit==next_pos),0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit = True
                elif event.type == 3:
                    if event.key == 273:
                        player.change_dir(up)
                    elif event.key == 274:
                        player.change_dir(down)
                    elif event.key == 275:
                        player.change_dir(right)
                    elif event.key == 276:
                        player.change_dir(left)

def toggle_fullscreen(screen,size,alreadyFull):
        if alreadyFull:
            screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode(size)
        return screen

game()
