import pygame
import random

from snake import snakeClass
from snake import snakeSprite
from food import foodClass
from snakeCommand import *
from buttons import Button
from constants import *
from controls import *

def eat_food(snake,food_list):
    eaten = 0
    for (x,y) in snake.snake_body:
        for food in food_list:
            if food.position == (x, y):
                snake.snake_length += 1
                ev = pygame.event.Event(GAME_EVENT, {'txt': "mmmnhami"})
                pygame.event.post(ev)
                print("Sent")
                ev = pygame.event.Event(GAME_EVENT, {'txt': "dammmm"})
                pygame.event.post(ev)
                food.move_food()
                eaten+=1
    return eaten

started = False

two_players = True

display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption('Snake')

background_color = (150,200,220)
pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 60)
font2 = pygame.font.Font('freesansbold.ttf', 20)

snake = snakeClass([(40, 20), (39, 20), (38, 20)],(1,0))
if two_players:
    snake2 = snakeClass([(40, 15), (39, 15), (38, 15)],(1,0))

snake_sprite = snakeSprite("snake_sprite.png",[pygame.rect.Rect(36,0,10,10), pygame.rect.Rect(48,12,10,10), pygame.rect.Rect(36,13,10,10),
                                                     pygame.rect.Rect(46,1,10,10), pygame.rect.Rect(13,1,10,10), pygame.rect.Rect(25,12,10,10),
                                                     pygame.rect.Rect(25,24,10,10), pygame.rect.Rect(25,1,10,10), pygame.rect.Rect(1,12,10,10),
                                                     pygame.rect.Rect(1,2,10,10), pygame.rect.Rect(36,24,10,10), pygame.rect.Rect(48,36,10,10),
                                                     pygame.rect.Rect(36,36,10,10), pygame.rect.Rect(48,24,10,10)])


snake_sprite2 = snakeSprite("snake_sprite2.png",[pygame.rect.Rect(36,0,10,10), pygame.rect.Rect(48,12,10,10), pygame.rect.Rect(36,13,10,10),
                                                     pygame.rect.Rect(46,1,10,10), pygame.rect.Rect(13,1,10,10), pygame.rect.Rect(25,12,10,10),
                                                     pygame.rect.Rect(25,24,10,10), pygame.rect.Rect(25,1,10,10), pygame.rect.Rect(1,12,10,10),
                                                     pygame.rect.Rect(1,2,10,10), pygame.rect.Rect(36,24,10,10), pygame.rect.Rect(48,36,10,10),
                                                     pygame.rect.Rect(36,36,10,10), pygame.rect.Rect(48,24,10,10)])

inputHandler_wasd = InputHandler(WASD)
inputHandler_arrows = InputHandler(ARROWS)


food_list=[]

points = 0

pause_sprite = pygame.image.load("pause.png")
play_sprite = pygame.image.load("play.png")


for i in range(0,3):
    if random.random() > 0.5:
        food_list.append(foodClass("apple.png"))
    else:
        food_list.append(foodClass("banana.png"))


def start_button_on_click():
    ev = pygame.event.Event(START_EVENT, {'txt': "mmmnhami"})
    pygame.event.post(ev)

start_button = Button(0,0,120,40,start_button_on_click,'Start')
start_button.centerButton(WIDTH//2*SCALE,HEIGHT//2*SCALE)

start_text = font.render('Snake', True, (250, 250, 250))
start_textRect = start_text.get_rect()
start_textRect.center = (WIDTH*SCALE//2, HEIGHT*SCALE//2 - 100)

GAME_EVENT = pygame.event.custom_type()
START_EVENT = pygame.event.custom_type()
GAMEOVER_EVENT = pygame.event.custom_type()

running = True
paused = False
quit = False

while not started and running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            quit = True
        elif event.type == START_EVENT:
            started = True
        
        start_button.handle_event(event)

    display.fill(background_color)
    display.blit(start_text, start_textRect)
    start_button.draw(display)

    # update window
    pygame.display.flip()
    clock.tick(15)


while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            quit = True
        elif event.type == pygame.KEYDOWN:

            command = inputHandler_wasd.handleInput(event)
            command.execute(command,snake)
            if two_players:
                command = inputHandler_arrows.handleInput(event)
                command.execute(command,snake2)
                
            if event.key == pygame.K_SPACE:
                paused = not paused
        elif event.type == GAME_EVENT:
            print(event.txt)
                
    if not paused:
        display.fill(background_color)

        display.blit(pause_sprite, (SCALE, SCALE, 30, 30))

        points_text = font2.render(str(points), True, (250, 250, 250))
        display.blit(points_text, (SCALE,(HEIGHT-3)*SCALE))

        for food in food_list:
            food.display_food(display)

        points+=eat_food(snake,food_list)
        if two_players:
            points+=eat_food(snake2,food_list)
        running = snake.move_snake()
        if two_players:
            running = running and snake2.move_snake() and snake.collide([snake,snake2])

        snake_sprite.displaySnake(display,snake)
        if two_players:
            snake_sprite2.displaySnake(display,snake2)

        
        # update window
        pygame.display.flip()
        clock.tick(15)

    else:
        pygame.draw.rect(display, background_color, (SCALE, SCALE, 30, 30))
        display.blit(play_sprite, (SCALE, SCALE, 30, 30))
        pygame.display.flip()
        clock.tick(15)


gameover_text = font.render('Game Over', True, (250, 250, 250))
gameover_textRect = gameover_text.get_rect()
gameover_textRect.center = (WIDTH*SCALE//2, HEIGHT*SCALE//2 - 50)

gameover_text2 = font2.render('Press SPACE to quit', True, (250, 250, 250))
gameover_text2Rect = gameover_text2.get_rect()
gameover_text2Rect.center = (WIDTH*SCALE//2, HEIGHT*SCALE//2 + 50)

#game over screen
end_color = (200,0,0)
while not quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                quit = True
        elif event.type == GAME_EVENT:
            print(event.txt)

    display.fill(end_color)
    display.blit(gameover_text, gameover_textRect)
    display.blit(gameover_text2, gameover_text2Rect)
    pygame.display.flip()
    clock.tick(15)

pygame.quit()
