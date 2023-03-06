import pygame as pg 
from Constants import *
import random



class BOARD:
    def __init__(self, WIDTH_BOARD=400, HEIGHT_BOARD=400, WIDTH_CELL=40, screen_size = (800,600)):
        self.WIDTH_BOARD = WIDTH_BOARD
        self.HEIGHT_BOARD = HEIGHT_BOARD
        self.SPEED = WIDTH_CELL//4
        self.WIDTH_CELL = WIDTH_CELL
        self.CELL_ROWS, self.CELL_COLS = self.WIDTH_BOARD//self.WIDTH_CELL, self.HEIGHT_BOARD//self.WIDTH_CELL
        self.PADDING_WIDTH = (screen_size[0] - self.WIDTH_BOARD)//2
        self.PADDING_HEIGHT = (screen_size[1] - self.HEIGHT_BOARD)//2

        self.limit_board = {'x':[self.PADDING_WIDTH , screen_size[0] - self.PADDING_WIDTH ], 
                            'y':[self.PADDING_HEIGHT, screen_size[1] - self.PADDING_HEIGHT]}
        self.limit_center = {'x':[self.PADDING_WIDTH+self.WIDTH_CELL//2, screen_size[0] - self.PADDING_WIDTH-self.WIDTH_CELL//2 ], 
                            'y':[self.PADDING_HEIGHT+self.WIDTH_CELL//2, screen_size[1] - self.PADDING_HEIGHT-self.WIDTH_CELL//2]}

    def __repr__(self):
        pass

board = BOARD()

W = random.choice([400, 600])
WIDTH_BOARD, HEIGHT_BOARD = (W,W)
WIDTH_CELL = WIDTH_BOARD//20
CELL_ROWS, CELL_COLS = WIDTH_BOARD//WIDTH_CELL, HEIGHT_BOARD//WIDTH_CELL
speed = WIDTH_CELL//2
padding_width, padding_height = (WIDTH - WIDTH_BOARD)//2, (HEIGHT - HEIGHT_BOARD)//2

limit_center = {'x':[padding_width+WIDTH_CELL//2, WIDTH-padding_width-WIDTH_CELL//2], 
                'y':[padding_height+WIDTH_CELL//2, HEIGHT-padding_height-WIDTH_CELL//2]}
limit_board = {'x':[padding_width, WIDTH-padding_width], 
               'y':[padding_height, HEIGHT-padding_height]}

#Function to check whether the ball can go on
def Go_on(coord, blocks, key):
    if key == pg.K_UP:
        if coord['y'] > limit_center['y'][0] and (coord['x'], coord['y'] - WIDTH_CELL) not in blocks:
            return True
    elif key == pg.K_DOWN:
        if coord['y'] < limit_center['y'][1] and (coord['x'], coord['y'] + WIDTH_CELL) not in blocks:
            return True
    elif key == pg.K_LEFT:
        if coord['x'] > limit_center['x'][0] and (coord['x'] - WIDTH_CELL, coord['y']) not in blocks:
            return True
    elif key == pg.K_RIGHT: 
        if coord['x'] < limit_center['x'][1] and (coord['x'] + WIDTH_CELL, coord['y']) not in blocks:
            return True
    
    return False
def drawing_block(screen, list_blocks):
    for (x, y) in list_blocks:
        pg.draw.rect(screen, GREY, pg.Rect(x-WIDTH_CELL//2,y-WIDTH_CELL//2, WIDTH_CELL, WIDTH_CELL))
def init_original_ball(list_blocks):
    while True:
        #Initilizatinal coordinate of ball and speed of ball
        init_x = random.choice([i for i in range(1, CELL_ROWS*2) if i % 2 == 1])
        init_y = random.choice([i for i in range(1, CELL_COLS*2) if i % 2 == 1])
        cord_circle = dict((('x',init_x * WIDTH_CELL//2 + padding_width), ('y',init_y*WIDTH_CELL//2 + padding_height))) 
        if (cord_circle['x'], cord_circle['y']) not in list_blocks:
            break
    return cord_circle
def drawing_line(screen, color = RED, width = 1):
    for c in range(0, CELL_COLS + 1):
        pg.draw.line(screen,color, (c*WIDTH_CELL+padding_width, padding_height),
                                    (c*WIDTH_CELL+padding_width, HEIGHT-padding_height), width = width)
    for r in range(0, CELL_ROWS + 1):
        pg.draw.line(screen,color, (padding_width, r*WIDTH_CELL+padding_height),
                                    (WIDTH-padding_width,r*WIDTH_CELL+padding_height), width=width)
def fill_rect(screen, original_coord, end_coord, color = YELLOW):
    rect_left = original_coord[0] if original_coord[0] <= end_coord[0] else end_coord[0]
    rect_top  = original_coord[1] if original_coord[1] <= end_coord[1] else end_coord[1]
    w, h = abs(end_coord[0] - original_coord[0]), abs(end_coord[1] - original_coord[1])
    screen.fill(color, pg.Rect(rect_left, rect_top, w, h))

def main_game(screen, clock, human_draw_blocks = False, lst_blocks_of_human = []):
    #Install background
    background_image = pg.image.load("images/Game_start.png").convert()
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))
    screen.fill(WHITE, pg.Rect(padding_width, padding_height, WIDTH_BOARD, HEIGHT_BOARD))
    
    #Drawing blocks
    amount_blocks = random.choice(range(100, 150))
    #list_blocks conttain list of center blocks
    list_blocks = random.choices([(x*WIDTH_CELL+WIDTH_CELL//2 + padding_width, y*WIDTH_CELL+WIDTH_CELL//2 + padding_height) for x in range(0, CELL_ROWS) for y in range(0, CELL_COLS)], k = amount_blocks)
    if human_draw_blocks:
        list_blocks.clear()
        list_blocks = lst_blocks_of_human
    

    #INIT ORIGINAL COORD OF BALL
    cord_circle = init_original_ball(list_blocks)
    original_coord = (cord_circle['x']-WIDTH_CELL//2, cord_circle['y']-WIDTH_CELL//2)
    prev_key = []

    winning =False
    vistied_row_col = [set(), set()]

    running = True
    while running:

        drawing_block(screen, list_blocks)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                    break

                if Go_on(cord_circle, list_blocks, event.key):
                    if len(prev_key) == 0 or event.key == prev_key[-1]:
                        if event.key == pg.K_UP:
                            original_coord =(cord_circle['x']-WIDTH_CELL//2, cord_circle['y'] + WIDTH_CELL//2)
                            cord_circle['y'] -= speed
                        elif event.key == pg.K_DOWN:
                            original_coord =(cord_circle['x']-WIDTH_CELL//2, cord_circle['y']-WIDTH_CELL//2)
                            cord_circle['y'] += speed
                        elif event.key == pg.K_LEFT:
                            original_coord =(cord_circle['x']+WIDTH_CELL//2, cord_circle['y']-WIDTH_CELL//2)
                            cord_circle['x'] -= speed
                        elif event.key == pg.K_RIGHT:
                            original_coord =(cord_circle['x']-WIDTH_CELL//2, cord_circle['y']-WIDTH_CELL//2)
                            cord_circle['x'] += speed
                        prev_key.append(event.key)

        if len(prev_key) != 0:
            if Go_on(cord_circle, list_blocks, prev_key[-1]):
                if prev_key[-1] == pg.K_UP:
                    cord_circle['y'] -= speed
                    end_coord = (cord_circle['x']+WIDTH_CELL//2,cord_circle['y'])
                elif  prev_key[-1] == pg.K_DOWN:
                    cord_circle['y'] += speed
                    end_coord = (cord_circle['x']+WIDTH_CELL//2,cord_circle['y'])
                elif prev_key[-1] == pg.K_LEFT:
                    cord_circle['x'] -= speed
                    end_coord = (cord_circle['x'],cord_circle['y']+WIDTH_CELL//2)
                elif prev_key[-1] == pg.K_RIGHT:
                    cord_circle['x'] += speed
                    end_coord = (cord_circle['x'],cord_circle['y']+WIDTH_CELL//2)
                fill_rect(screen, original_coord, end_coord)
            else:
                
                prev_key.clear()
        
        drawing_line(screen)
        pg.draw.circle(screen, BLUE, (cord_circle['x'], cord_circle['y']) , WIDTH_CELL//4)
        
        pg.display.flip()
        clock.tick(60)


