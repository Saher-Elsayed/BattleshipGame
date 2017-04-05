import pygame, sys, random, copy
import time
from pygame.locals import *

pygame.init()
display_width = 600
display_height = 600
board_width = display_width * 0.7
board_height = display_height * 0.7
xpos = display_width * 0.15
count = []
check = 410
ypos = display_height * 0.1
tilesize = 40
markersize = 40
TEXT_HEIGHT = 25
r_speed = 8
TEXT_LEFT_POSN = 10
NUMBER_OF_SHIPS = 10

images = [
	pygame.image.load("img/blowup1.png"), pygame.image.load("img/blowup2.png"),
	pygame.image.load("img/blowup3.png"),pygame.image.load("img/blowup4.png"),
	pygame.image.load("img/blowup5.png"),pygame.image.load("img/blowup6.png")]

black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 50, 255)
violet = (102, 0, 104)
white = (255, 255, 255)
cobalt = (0, 0, 204)
green = (0, 200, 0)
light_green = (0, 255, 0)

bgcolor = violet
tilecolor = green

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Battleship")
clock = pygame.time.Clock()
battleshipimg = pygame.image.load("img/battleship.png")

def text_objects(text, font, colour):
	textSurface = font.render(text, True, colour)
	return textSurface, textSurface.get_rect()

def getboard(value):
	return [[value]*10 for i in xrange(10)]

def help():
	BASICFONT = pygame.font.Font("freesansbold.ttf", 20)
	exit = False
	while (not exit):
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				exit = True
		gameDisplay.fill(bgcolor)
		line2_surf, line2_rect = text_objects('The objective is to sink all the ships in as few shots as', BASICFONT, white)
		line2_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 3)
		gameDisplay.blit(line2_surf, line2_rect)

		line3_surf, line3_rect = text_objects('possible.', BASICFONT, white)
		line3_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 4)
		gameDisplay.blit(line3_surf, line3_rect)

		linex_surf, linex_rect = text_objects('The markers on the edges of the game board tell you how', BASICFONT, white)
		linex_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 7)
		gameDisplay.blit(linex_surf, linex_rect)

		line4_surf, line4_rect = text_objects('many ship pieces are in each column and row.', BASICFONT, white)
		line4_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 8)
		gameDisplay.blit(line4_surf, line4_rect)

		line5_surf, line5_rect = text_objects('To reset the game press any button', BASICFONT, white)
		line5_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 10)
		gameDisplay.blit(line5_surf, line5_rect)

		while keypress() == None:
			pygame.display.update()
			clock.tick(30)
		main_scr()

def exit_game():
	pygame.quit()
	quit()

def button(msg,x,y,w,h,ic,ac,txtcolor,action=None):
	goBack = False
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if (x+w > mouse[0] > x and y+h > mouse[1] > y):
		pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
		if (click[0] == 1 and action != None):
			action()
	else:
		pygame.draw.rect(gameDisplay, ic, (x,y,w,h))
	# ketan told me to leave it

	smallText = pygame.font.Font("freesansbold.ttf", 20)
	textSurf, textRect = text_objects(msg, smallText, txtcolor)
	textRect.center = ((x+(w/2)), (y+(h/2)))
	gameDisplay.blit(textSurf, textRect)

def add_ships(board, ships, numberOfShips):
	ship_length = 0

	for i in range(numberOfShips):
		valid_ship_position = False
		while not valid_ship_position:
			xStartpos = random.randint(0, 9)
			yStartpos = random.randint(0, 9)
			isHorizontal = random.randint(0, 1)
			ship = ships.keys()[random.randint(0,len(ships)-1)]
			ship_length = ships[ship]

			valid_ship_position, ship_coords = ship_pos(board, xStartpos, yStartpos, isHorizontal, ship_length, ship)
			if valid_ship_position:
				for coord in ship_coords:
					board[coord[0]][coord[1]] = ship
	return board

def ship_pos(board, xPos, yPos, isHorizontal, length, ship):
	ship_coordinates = []
	if isHorizontal:
		for i in xrange(length):
			if (i+xPos > 9) or (board[i+xPos][yPos] != None) or hasAdjacent(board, i+xPos, yPos, ship):
				return (False, ship_coordinates)
			else:
				ship_coordinates.append((i+xPos, yPos))
	else:
		for i in xrange(length):
			if (i+yPos > 9) or (board[xPos][i+yPos] != None) or hasAdjacent(board, xPos, i+yPos, ship):
				return (False, ship_coordinates)
			else:
				ship_coordinates.append((xPos, i+yPos))
	return (True, ship_coordinates)

def hasAdjacent(board, xPos, yPos, ship):
    for x in xrange(xPos-1,xPos+2):
        for y in xrange(yPos-1,yPos+2):
            if (x in range(10)) and (y in range(10)) and (board[x][y] not in (ship, None)):
                return True
    return False

def draw_board(board, revealed):
	for tilex in xrange(10):
		for tiley in xrange(10):
			left, top = left_top_coords(tilex, tiley)
			if not revealed[tilex][tiley]:
				pygame.draw.rect(gameDisplay,tilecolor,(left,top,tilesize,tilesize))
			else:
				if board[tilex][tiley] != None:
					pygame.draw.rect(gameDisplay, red, (left,top,tilesize,tilesize))

	for x in xrange(0, (11)*tilesize, tilesize):
		pygame.draw.line(gameDisplay,black,(x+xpos+markersize-40, ypos+markersize-40), (x+xpos+markersize-40, display_height-ypos-80))
	for y in xrange(0, (11)*tilesize, tilesize):
		pygame.draw.line(gameDisplay,black,(xpos+markersize-40, y+ypos+markersize-40), (display_width-(markersize*2)-30, y+ypos+markersize-40))

def draw_markers(xlist, ylist):
	smallText = pygame.font.Font("freesansbold.ttf", 20)
	for i in xrange(len(xlist)):
		left = i * markersize + xpos + markersize + (tilesize / 3) - 40
		top = ypos - 40
		marker_surf, marker_rect = text_objects(str(xlist[i]), smallText, white)
		marker_rect.topleft = (left, top)
		gameDisplay.blit(marker_surf, marker_rect)
	for i in xrange(len(ylist)):
		left = xpos - 40
		top = i * markersize + ypos + markersize + (tilesize/3) - 40
		marker_surf, marker_rect = text_objects(str(ylist[i]), smallText, white)
		marker_rect.topleft = (left, top)
		gameDisplay.blit(marker_surf, marker_rect)

def set_markers(board):
	xmarkers = [0 for i in xrange(10)]
	ymarkers = [0 for i in xrange(10)]
	for tilex in xrange(10):
		for tiley in xrange(10):
			if board[tilex][tiley] != None:
				xmarkers[tilex] += 1
				ymarkers[tiley] += 1
	return (xmarkers, ymarkers)

def left_top_coords(tilex, tiley):
	left = tilex * tilesize + xpos + markersize - 40
	top = tiley * tilesize + ypos + markersize - 40
	return (left, top)

def get_pixel(x, y):
	for tilex in xrange(10):
		for tiley in xrange(10):
			left, top = left_top_coords(tilex, tiley)
			tile_rect = pygame.Rect(left, top, tilesize, tilesize)
			if tile_rect.collidepoint(x, y):
				return(tilex, tiley)
	return (None, None)

def highlight_tile(tilex, tiley):
	left, top = left_top_coords(tilex, tiley)
	pygame.draw.rect(gameDisplay, blue,(left,top,tilesize,tilesize), 4)

def reveal_animation(board, tile):
	for x in xrange(tilesize, (-r_speed) - 1, -r_speed):
		draw_tile_covers(board, tile, x)

def draw_tile_covers(board, tile, x):
	left, top = left_top_coords(tile[0][0], tile[0][1])
	if check_revealed_tile(board, tile):
		pygame.draw.rect(gameDisplay, red, (left,top,tilesize,tilesize))
	else:
		pygame.draw.rect(gameDisplay, bgcolor, (left,top,tilesize,tilesize))
	if x > 0:
		pygame.draw.rect(gameDisplay, tilecolor, (left,top,x,tilesize))
	pygame.display.update()
	clock.tick(30)

def check_revealed_tile(board, tile):
	return (board[tile[0][0]][tile[0][1]] != None)

def blowup(tile):
	for img in images:
		img = pygame.transform.scale(img, (tilesize+5, tilesize))
		gameDisplay.blit(img, tile)
		pygame.display.update()
		clock.tick(10)

def win(board, revealed):
	for x in xrange(10):
		for y in xrange(10):
			if board[x][y] != None and not revealed[x][y]:
				return False
	return True

def gameover_scr(shots):
	BASICFONT = pygame.font.Font("freesansbold.ttf", 20)
	gameDisplay.fill(bgcolor)
	counter_surf, counter_rect = text_objects("Shots : " + str(shots), BASICFONT, white)
	counter_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 2)
	gameDisplay.blit(counter_surf, counter_rect)

	line2_surf, line2_rect = text_objects('CONGRATS!!', BASICFONT, white)
	line2_rect.topleft = (TEXT_LEFT_POSN+200, TEXT_HEIGHT * 6)
	gameDisplay.blit(line2_surf, line2_rect)

	line3_surf, line3_rect = text_objects('Press any button to exit', BASICFONT, white)
	line3_rect.topleft = (TEXT_LEFT_POSN+150, TEXT_HEIGHT * 8)
	gameDisplay.blit(line3_surf, line3_rect)
	while keypress() == None:
		pygame.display.update()
		clock.tick(30)
	exit_game()

def keypress():
	for event in pygame.event.get([KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION]):
	    if event.type in (KEYDOWN, MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION):
	        continue
	    return event.key
	return None

def start_game():
	board_ship = getboard(None)
	revealed_ship = getboard(False)
	ship_objs = {'battleship':4,'cruiser':3,'destroyer':2}
	button_width = board_width/5.0
	button_height = (display_height - ypos - board_height)/3.0
	board_ship = add_ships(board_ship, ship_objs, NUMBER_OF_SHIPS)
	gameDisplay.fill(bgcolor)
	xmarkers, ymarkers = set_markers(board_ship)
	mousex, mousey = 0, 0
	mouse_clicked = False
	names = {1:"NEW",3:"EXIT"}
	funct = {1:main_scr,3:exit_game}
	exit = False
	while (not exit):
		click = pygame.mouse.get_pressed()
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				exit = True
			mousex, mousey = pygame.mouse.get_pos()
			if click[0] == 1:
				mouse_clicked = True
			else:
				mouse_clicked = False
		tilex, tiley = get_pixel(mousex, mousey)
		draw_board(board_ship, revealed_ship)
		draw_markers(xmarkers, ymarkers)
		if tilex != None and tiley != None:
			if not revealed_ship[tilex][tiley]:
				highlight_tile(tilex, tiley)
			if not revealed_ship[tilex][tiley] and mouse_clicked:
				reveal_animation(board_ship, [(tilex, tiley)])
				revealed_ship[tilex][tiley] = True
				if check_revealed_tile(board_ship, [(tilex, tiley)]):
					left, top = left_top_coords(tilex, tiley)
					blowup([left, top])
					if win(board_ship, revealed_ship):
						count.append((tilex,tiley))
						gameover_scr(len(count))
				count.append((tilex,tiley))
		for x in names:
			button(names[x],xpos + button_width*x,ypos + board_height + button_height,button_width,button_height,green,red,white,funct[x],)
		pygame.display.update()
		clock.tick(30)
	pygame.quit()

def icon(x, y):
	gameDisplay.blit(battleshipimg, (x, y))

def main_scr():
	x = (display_width * 0.25)
	y = (display_height * 0.15)
	gameExit = False
	while (not gameExit):
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				exit_game()
				gameExit = True
		gameDisplay.fill(cobalt)
		icon(x, y)
		button("PLAY",250,450,100,50,green,light_green,white,start_game)
		button("HELP",250,510,100,50,green,light_green,white,help)
		pygame.display.update()
		clock.tick(30)

main_scr()
pygame.quit()
quit()
