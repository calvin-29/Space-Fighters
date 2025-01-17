import pygame
from pygame.locals import *
from sys import exit

pygame.init()

screen = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption("Joy Sticks")
font = pygame.font.SysFont("Futara", 25)
clock = pygame.time.Clock()
col = (10, 50, 70)
x = 320-35
y = 240-35
joysticks = []

def draw(text, font, col, x, y):
    img = font.render(text, 1, col)
    screen.blit(img, (x, y))

while True:
    screen.fill((0, 0, 0))
    draw("Controllers Connected : " + str(pygame.joystick.get_count()), font, (200, 10, 200), 30, 10)
    
    for joystick in joysticks:
        draw("Controller Type : " + str(joystick.get_name()), font, (200, 10, 200), 30, 40)
        draw("Battery Level : " + str(joystick.get_power_level()), font, (200, 10, 200), 30, 70)
        draw("Number of axes : " + str(joystick.get_numaxes()), font, (200, 10, 200), 30, 100)
    
    for joystick in joysticks:
        if joystick.get_button(0):
            col = (10, 150, 70)
        if joystick.get_button(1):
            col = (10, 150, 170)
        if joystick.get_button(2):
            col = (110, 150, 170)
        if joystick.get_button(3):
            col = (110, 10, 170)
        
        if joystick.get_hat(0)[0] == 1:
            x+=10
        if joystick.get_hat(0)[0] == -1:
            x-=10
        if joystick.get_hat(0)[1] == 1:
            y-=10
        if joystick.get_hat(0)[1] == -1:
            y+=10
        
        horiz_move = joystick.get_axis(0)
        vert_move = joystick.get_axis(1)
        if abs(vert_move) > 0.05:
            y += vert_move * 2
        if abs(horiz_move) > 0.05:
            x += horiz_move * 2
    
    rect = pygame.Rect(x, y, 70, 70)
    pygame.draw.rect(screen, col, rect, border_radius=10)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            joy.init()
            joysticks.append(joy)
    
    clock.tick(60)
    pygame.display.update()
