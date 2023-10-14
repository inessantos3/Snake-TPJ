import pygame

pygame.font.init()
COLOR_INACTIVE = pygame.Color(255,255,255)
COLOR_ACTIVE = pygame.Color(50,100,200)
FONT = pygame.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, text='', max_length=10):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.max_length = max_length
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < self.max_length:
                        self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Button:

    def __init__(self,x,y,w,h,onClick,text='',fontSize = 32):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.enabled = True
        self.OnClick = onClick
        self.font = pygame.font.Font(None, fontSize)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.disabled = False
    
    def updateText(self,text):
        self.text = text
        self.txt_surface = self.txt_surface = FONT.render(text, True, self.color)

    def centerButton(self,x,y):
        self.rect.center = (x,y)
        self.txt_surface.get_rect().center = (x,y)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # execute onClick
                self.OnClick()
                self.color = COLOR_ACTIVE
            else:
                self.color = COLOR_INACTIVE

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+(self.rect.width-self.txt_surface.get_rect().width)/2, self.rect.y+(self.rect.height-self.txt_surface.get_rect().height)/2))
        pygame.draw.rect(screen, self.color, self.rect, 2)

