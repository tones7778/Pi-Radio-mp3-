import sys, pygame
from pygame.locals import *
import time
import datetime
import subprocess
import os
import glob
import random

pygame.init()

#define colors
cyan = 50, 255, 255
blue = 26, 0, 255
black = 0, 0, 0
white = 255, 235, 235
red = 255, 0, 0
green = 0, 255, 0

#other
subprocess.call("mpc random off", shell=True)
subprocess.call("mpc volume 60", shell=True)
shuffle = False

_image = ['200x170.png','200x170b.png','200x170c.png','200x170d.png']
next_image = random.choice(_image)

#define function that checks for mouse location
def on_click():
	click_pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
	#check to see if exit has been pressed
	if 500 <= click_pos[0] <= 615 and 20 <= click_pos[1] <=73:
		print "You pressed exit" 
		button(0)
	#now check to see if play was pressed
	if 178 <= click_pos[0] <= 327 and 410 <= click_pos[1] <=460:
                print "You pressed button play"
                button(1)
	#now check to see if stop  was pressed
        if 320 <= click_pos[0] <= 473 and 410 <= click_pos[1] <460:
                print "You pressed button stop"
                button(2)
	#now check to see if refreshed  was pressed
        if 360 <= click_pos[0] <= 475 and 20 <= click_pos[1] <=73:
                print "You pressed button mp3"
                button(3)
	#now check to see if previous  was pressed
        if 24 <= click_pos[0] <= 178 and 410 <= click_pos[1] <=460:
                print "You pressed button previous"
                button(4)

	 #now check to see if next  was pressed
        if 473 <= click_pos[0] <= 620 and 410 <= click_pos[1] <=460:
                print "You pressed button next"
                button(5)

	 #now check to see if volume down was pressed
        if 25 <= click_pos[0] <= 135 and 20 <= click_pos[1] <=73:
                print "You pressed volume down"
                button(6)

	 #now check to see if button 7 was pressed
        if 135 <= click_pos[0] <= 254 and 20 <= click_pos[1] <=73:
                print "You pressed volume up"
                button(7)

	 #now check to see if button 8 was pressed
        if 247 <= click_pos[0] <= 365 and 20 <= click_pos[1] <=73:
                print "You pressed radio"
                button(8)

	 #now check to see if button 9 was pressed
        if 500 <= click_pos[0] <= 615 and 100 <= click_pos[1] <=150:
                print "You pressed shuffle"
                button(9)


#define action on pressing buttons
def button(number):
	print "You pressed button ",number
	if number == 0:    #specific script when exiting
		screen.fill(black)
		font=pygame.font.Font(None,44)
        	label=font.render("Radioplayer will continue in background", 1, (white))
        	screen.blit(label,(20,180))
		pygame.display.flip()
		time.sleep(3)
		sys.exit()

	if number == 1:	
		subprocess.call("mpc play ", shell=True)
		refresh_menu_screen()

	if number == 2:
		subprocess.call("mpc stop ", shell=True)
		refresh_menu_screen()

	if number == 8:
		subprocess.call("mpc clear ", shell=True)
		subprocess.call("mpc load playlist ", shell=True)
		refresh_menu_screen() 

	if number == 4:
		subprocess.call("mpc prev ", shell=True)
		refresh_menu_screen()

	if number == 5:
		subprocess.call("mpc next ", shell=True)
	        next_image = random.choice(_image)
		refresh_menu_screen()

	if number == 6:
		subprocess.call("mpc volume -5 ", shell=True)
		refresh_menu_screen()

	if number == 7:
		subprocess.call("mpc volume +5 ", shell=True)
		refresh_menu_screen()

	if number == 9:
                subprocess.call("mpc random ", shell=True)
		global shuffle
		shuffle = (1,0)[shuffle]
		refresh_menu_screen()

        if number == 3:
                subprocess.call("mpc clear ", shell=True)
		subprocess.call("mpc load mp3 ", shell=True)
                refresh_menu_screen()


def refresh_menu_screen():
#set up the fixed items on the menu
	#screen.fill(black) #change the colours if needed
        current_time = datetime.datetime.now().strftime('%I:%M')
        time_font=pygame.font.Font(None,100)
        time_label = time_font.render(current_time, 1, (cyan))

	font=pygame.font.Font(None,50)
	station_font=pygame.font.Font(None,40)
        skin=pygame.image.load("skin.png")
	indicator_on=font.render("[       ]", 1, (blue))
        indicator_off=font.render("", 1, (white))
	label2=font.render("Internet Radio", 1, (cyan))
	#draw the main elements on the screen
	image=pygame.image.load(next_image)
        screen.blit(skin,(0,0))
        screen.blit(image,(25,90))
        #screen.blit(label,(520, 105))
        screen.blit(label2,(250, 100))
	pygame.draw.rect(screen, black, (447, 167, 178, 69),0)
	pygame.draw.rect(screen, black, (70, 267, 545, 120),0)
        screen.blit(time_label,(450, 165))

	##### display the station name and split it into 2 parts : 
	lines = subprocess.check_output("mpc current", shell=True).split(":")

	if len(lines)==1:
		line1 = lines[0]
		line1 = line1[:-1]
		line2 = "No additional info: "
	else:
		line1 = lines[0]
		line2 = lines[1]

	line1 = line1[:38]
	line2 = line2[:38]
	line2 = line2[:-1]
	#trap no station data
	if line1 =="":
		line2 = "Press PLAY"
		station_status = "Stopped"
		status_font = red
	else:
		station_status = "Playing"
		status_font = green
	station_name=station_font.render(line1, 1, (white))
	additional_data=station_font.render(line2, 1, (white))
	station_label=font.render(station_status, 1, (status_font))
	screen.blit(station_label,(250,205)) #playing
	screen.blit(station_name,(70,350))
	screen.blit(additional_data,(70,280))
	######## add volume number
	volume = subprocess.check_output("mpc volume", shell=True )
	volume = volume[8:]
	volume = volume[:-1]
	volume_tag=font.render(volume, 1, (white))
	screen.blit(volume_tag,(250,150))
	####### check to see if the Radio is connected to the internet
	IP = subprocess.check_output("hostname -I", shell=True )
	IP=IP[:3]
	if IP =="192":
		network_status = "online"
		status_font = green

	else:
		network_status = "offline"
		status_font = red
	###### check for random
	if shuffle == 1:
		screen.blit(indicator_on,(517, 102))

	else:
        	screen.blit(indicator_off,(517, 102))

	network_status_label = font.render(network_status, 1, (status_font))
	screen.blit(network_status_label, (330,150))
	pygame.display.flip()


def main():
        while 1:
                for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                print "screen pressed" #for debugging purposes
                                pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
                                print pos #for checking
                                pygame.draw.circle(screen, red, pos, 2, 0) #for debugging purposes - adds a small dot where the screen is pressed
                                on_click()

#ensure there is always a safe way to end the program if the touch screen fails

                        if event.type == KEYDOWN:
                                if event.key == K_ESCAPE:
                                        sys.exit()

		refresh_menu_screen()

	refresh_menu_screen()
	time.sleep(0.2)


#################### EVERTHING HAS NOW BEEN DEFINED ###########################

#set size of the screen
size = width, height = 640, 480
screen = pygame.display.set_mode((size),pygame.FULLSCREEN)
#station_name()
refresh_menu_screen()  #refresh the menu interface 
main() #check for key presses and start emergency exit


