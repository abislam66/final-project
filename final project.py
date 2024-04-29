import pygame
import random
pygame.init()
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('kitty')
clock = pygame.time.Clock()
FPS=60
g=1
max_platforms = 10
scroll_thres= 200
scroll= 0
bg_scroll = 0




white=(255,255,255)
bob_image = pygame.image.load('kitty.png').convert_alpha()
bg_image=pygame.image.load('bg2.webp').convert_alpha()
platform_image=pygame.image.load('wood2.png').convert_alpha()

def draw_bg (bg_scroll):
    screen.blit(bg_image,(0,0+bg_scroll))
    screen.blit(bg_image,(0,-600+bg_scroll))
class player():
    
    def __init__(self,x,y):
        self.image = pygame.transform.scale(bob_image, (70,50))
        self.width = 40
        self.height = 40
        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.center = (x,y)
        self.vel_y = 0
        self.flip = False
        
        self.rect.center= (x,y)
    

    def move(self):
        scroll = 0
        dx = 0
        dy = 0
        
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx  = -10
            self.flip = True
        if key[pygame.K_d]:
            dx = +10
            self.flip= False
        self.vel_y+=g
        dy += self.vel_y
     
        if self.rect.left + dx <0:
            dx = 0-self.rect.left
        if self.rect.right + dx> screen_width:
            dx = screen_width - self.rect.right
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy,self.width,self.height):
                if self.rect.bottom<platform.rect.centery:
                    if self.vel_y:
                        self.rect.bottom = platform.rect.top
                        dy=0
                        self.vel_y = -20
                        
        if self.rect.bottom+dy>screen_height:
            dy = 0
            self.vel_y = -10
        if self.rect.top <= scroll_thres:
            if self.vel_y<0:
                scroll = -dy
          
        self.rect.x +=dx
        self.rect.y += dy +scroll

        
        return scroll
    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.flip, False), (self.rect.x-10,self.rect.y))
        pygame.draw.rect(screen,white,self.rect,1)
        

class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,width):
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.transform.scale(platform_image, (width,10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self, scroll):
        self.rect.y +=scroll





            
bob = player(screen_width//2,screen_height-150)
platform_group= pygame.sprite.Group()
for p in range(max_platforms):
    p_w = random.randint(40,60)
    p_x = random.randint(0,screen_width-p_w)
    p_y = p * random.randint(50,120)
    platform = Platform(p_x,p_y, p_w)
    platform_group.add(platform)

        













run = True
while run:
    clock.tick(FPS)
    
    scroll = bob.move()
    bg_scroll += scroll
    draw_bg(scroll)
    if bg_scroll>=600:
        bg_scroll = 0
    draw_bg(bg_scroll)
    pygame.draw.line(screen, white,(0,scroll_thres),(screen_width,scroll_thres))
    platform_group.update(scroll)
    platform_group.draw(screen)
    
##    screen.blit(bg_image,(0,0))
    bob.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

    pygame.display.update()
