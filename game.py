import pygame
import time

pygame.init()
display_width = 600
display_height = 600
board_width = display_width * 0.7
board_height = display_height * 0.7
xpos = display_width * 0.15
ypos = display_height * 0.1
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)
scr = (0, 0, 204)
green = (0, 200, 0)
light_green = (0, 255, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Battleship")
clock = pygame.time.Clock()
battleshipimg = pygame.image.load("battleship.png")
#func to create text
def text_objects(text, font):
	textSurface = font.render(text, True, white)
	return textSurface, textSurface.get_rect()
#func to return board list
def getboard():
	b = []
	col = ([0, ] * 10)
	for i in range(0, 10):
		b.append(col)
	return b
#func to display instructions
def help():
	exit = False
	while (not exit):
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				exit = True
		gameDisplay.fill(white)
		
		pygame.display.update()
		clock.tick(60)
	pygame.quit()
#func to create a button
def button(msg,x,y,w,h,ic,ac,action=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if (x+w > mouse[0] > x and y+h > mouse[1] > y):
		pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
		if (click[0] == 1 and action != None):
			action()
	else:
		pygame.draw.rect(gameDisplay, ic, (x,y,w,h))
	smallText = pygame.font.Font("freesansbold.ttf", 20)
	textSurf, textRect = text_objects(msg, smallText)
	textRect.center = ((x+(w/2)), (y+(h/2)))
	gameDisplay.blit(textSurf, textRect)

#func to start gameboard
def start_game():
	exit = False
	while (not exit):
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				exit = True
		gameDisplay.fill(white)
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		board_ship = getboard()
		board_grid = getboard()
		pygame.draw.rect(gameDisplay, green, (xpos,ypos,board_width,board_height))
		button_width = board_width/5.0
		button_height = (display_height - ypos - board_height)/3.0
		names = {0:"HELP",2:"RESET",4:"EXIT"}
		funct = {0:help,2:None,4:None}
		for x in names:
			button(names[x],xpos + button_width*x,ypos + board_height + button_height,button_width,button_height,green,red,funct[x])
		pygame.display.update()
		clock.tick(60)
	pygame.quit()
#func to display the icon
def icon(x, y):
	gameDisplay.blit(battleshipimg, (x, y))
#func for main screen
def main_scr():
	x = (display_width * 0.3)
	y = (display_height * 0.19)

	gameExit = False
	while (not gameExit):
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				gameExit = True
		gameDisplay.fill(scr)
		icon(x, y)
		button("PLAY",340,450,100,50,green,light_green,start_game)
		pygame.display.update()
		clock.tick(60)

main_scr()
pygame.quit()
quit()
