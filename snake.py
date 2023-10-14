import pygame
from constants import *

class Actor:
    def up():
        raise NotImplemented
    def down():
        raise NotImplemented
    def left():
        raise NotImplemented
    def right():
        raise NotImplemented

class snakeClass(Actor):
    def __init__(self,body,direction,rainbow=False,color=(250,0,0)):
        self.snake_body = body
        self.snake_direction = direction
        self.snake_length = len(body)
        self.snake_color = color
        self.rainbow = rainbow

    def getBody(self):
        return self.snake_body
    
    def getDirection(self):
        return self.snake_direction

    def increase_length(self,value=1):
        self.snake_length+=value

    def set_direction(self,direction):
        new_direction = self.snake_direction
        match direction:
            case "up":
                new_direction = (0,-1)
            case "down":
                new_direction = (0,1)
            case "left":
                new_direction = (-1,0)
            case "right":
                new_direction = (1,0)

        if self.snake_direction[0]*new_direction[0] >= 0 and self.snake_direction[1]*new_direction[1] >= 0:
            self.snake_direction = new_direction

    def up(self):
        self.set_direction("up")

    def down(self):
        self.set_direction("down")

    def left(self):
        self.set_direction("left")

    def right(self):
        self.set_direction("right")


    def move_snake(self):
        for (x,y) in self.snake_body:
            if x not in range(WIDTH) or y not in range(HEIGHT):
                print("Snake crashed against the wall")
                return False

            if self.snake_body.count((x, y)) > 1:
                print("Snake eats self")
                return False
        
        self.snake_body[0:0] = [
            (self.snake_body[0][0] + self.snake_direction[0], self.snake_body[0][1] + self.snake_direction[1])
        ]
        while len(self.snake_body) > self.snake_length:
            self.snake_body.pop()
        
        return True

    def collide(self,other_snakes):
        all_snakes = []
        for snake in other_snakes:
            all_snakes += snake.getBody()
        for x,y in all_snakes:
            if all_snakes.count((x, y)) > 1:
                print("Snake collided with another")
                return False
        return True

    def display_snake(self,display):
        if self.rainbow:
            self.snake_color = rainbow_color(self.snake_color)
        for x, y in self.snake_body:
            pygame.draw.rect(display, self.snake_color, (SCALE * x, SCALE * y, SCALE, SCALE))



def rainbow_color(prev_color):
    red = prev_color[0]
    green = prev_color[1]
    blue = prev_color[2]

    if prev_color[0] == 0:
        if green > 0:
            green-=1
        else:
            red = 1
            green = 0
        if blue < 255:
            blue+=1
        else:
            red = 1
            blue = 255
    elif prev_color[1] == 0:
        if blue > 0:
            blue-=1
        else:
            green = 1
            blue = 0
        if red < 255:
            red+=1
        else:
            green = 1
            red = 255

    elif prev_color[2] == 0:
        if red > 0:
            red-=1
        else:
            blue = 1
            red = 0
        if green < 255:
            green+=1
        else:
            blue = 1
            green = 255

    return (red,green,blue)

class snakeSprite(pygame.sprite.Sprite):

    def __init__(self,source_sprite,rectangles):
        pygame.sprite.Sprite.__init__(self)

        self.sprite = pygame.image.load(source_sprite)
        self.headup = self.sprite.subsurface(rectangles[0])
        self.headdown = self.sprite.subsurface(rectangles[1])
        self.headleft = self.sprite.subsurface(rectangles[2])
        self.headright = self.sprite.subsurface(rectangles[3])
        self.horizontal = self.sprite.subsurface(rectangles[4])
        self.vertical = self.sprite.subsurface(rectangles[5])
        self.left_to_up = self.sprite.subsurface(rectangles[6])
        self.left_to_down = self.sprite.subsurface(rectangles[7])
        self.right_to_up = self.sprite.subsurface(rectangles[8])
        self.right_to_down = self.sprite.subsurface(rectangles[9])
        self.tailup = self.sprite.subsurface(rectangles[10])
        self.taildown = self.sprite.subsurface(rectangles[11])
        self.tailleft = self.sprite.subsurface(rectangles[12])
        self.tailright = self.sprite.subsurface(rectangles[13])

    def displaySnake(self,display,snake):

        body = snake.getBody()
        
        prev_direction = snake.getDirection()
        next_direction = (0,0)

        match prev_direction:
            case (1,0):
                display.blit(self.headright,(body[0][0]*SCALE,body[0][1]*SCALE,SCALE,SCALE))
            case (-1,0):
                display.blit(self.headleft,(body[0][0]*SCALE,body[0][1]*SCALE,SCALE,SCALE))
            case (0,1):
                display.blit(self.headdown,(body[0][0]*SCALE,body[0][1]*SCALE,SCALE,SCALE))
            case (0,-1):
                display.blit(self.headup,(body[0][0]*SCALE,body[0][1]*SCALE,SCALE,SCALE))


        for i in range(1,len(body)-1):
            direction = (body[i-1][0]-body[i][0],body[i-1][1]-body[i][1])
            next_direction = (body[i][0]-body[i+1][0],body[i][1]-body[i+1][1])

            if(direction == next_direction):
                match next_direction:
                    case (1,0):
                        display.blit(self.horizontal,(body[i][0]*SCALE,body[i][1]*SCALE,SCALE,SCALE))
                    case (-1,0):
                        display.blit(self.horizontal,(body[i][0]*SCALE,body[i][1]*SCALE,SCALE,SCALE))
                    case (0,1):
                        display.blit(self.vertical,(body[i][0]*SCALE,body[i][1]*SCALE,SCALE,SCALE))
                    case (0,-1):
                        display.blit(self.vertical,(body[i][0]*SCALE,body[i][1]*SCALE,SCALE,SCALE))

            else:
                match (direction,next_direction):
                    case ((-1,0),(0,1)):
                        display.blit(self.left_to_up,(body[i][0]*SCALE,body[i][1]*SCALE,SCALE,SCALE))
                    case ((0,-1),(1,0)):
                        display.blit(self.left_to_up,(body[i][0]*SCALE,body[i][1]*SCALE,SCALE,SCALE))
                    case ((1,0),(0,1)):
                        display.blit(self.right_to_up,(body[i][0]*SCALE,body[i][1]*SCALE,SCALE,SCALE))
                    case ((0,-1),(-1,0)):
                        display.blit(self.right_to_up,(body[i][0]*SCALE,body[i][1]*SCALE,SCALE,SCALE))
                    case ((0,1),(1,0)):
                        display.blit(self.left_to_down,(body[i][0]*SCALE,body[i][1]*SCALE,SCALE,SCALE))
                    case ((-1,0),(0,-1)):
                        display.blit(self.left_to_down,(body[i][0]*SCALE,body[i][1]*SCALE,SCALE,SCALE))
                    case ((1,0),(0,-1)):
                        display.blit(self.right_to_down,(body[i][0]*SCALE,body[i][1]*SCALE,SCALE,SCALE))
                    case ((0,1),(-1,0)):
                        display.blit(self.right_to_down,(body[i][0]*SCALE,body[i][1]*SCALE,SCALE,SCALE))

            prev_direction = direction

        match next_direction:
            case (1,0):
                display.blit(self.tailright,(body[len(body)-1][0]*SCALE,body[len(body)-1][1]*SCALE,SCALE,SCALE))
            case (-1,0):
                display.blit(self.tailleft,(body[len(body)-1][0]*SCALE,body[len(body)-1][1]*SCALE,SCALE,SCALE))
            case (0,1):
                display.blit(self.taildown,(body[len(body)-1][0]*SCALE,body[len(body)-1][1]*SCALE,SCALE,SCALE))
            case (0,-1):
                display.blit(self.tailup,(body[len(body)-1][0]*SCALE,body[len(body)-1][1]*SCALE,SCALE,SCALE))
        


                