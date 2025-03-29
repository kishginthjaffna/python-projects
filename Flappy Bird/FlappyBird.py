# Flappy Bird in Python using Pygame

import pygame #pip install pygame
import os
import random

pygame.font.init()

# Window
width = 500
height = 800

bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird1.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird2.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird3.png")))]

pipe_image = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "pipe.png")))
base_image = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "base.png")))
background_image = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bg.png")))
game_over_image = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "GameOver.png")))
game_over_image = pygame.transform.scale(game_over_image, (300, 150))

stat_font = pygame.font.SysFont("comicsans", 25)

# Base Class
class Base:
    velocity = 5
    width = base_image.get_width()
    img = base_image

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.width
    
    def move(self):
        self.x1 -= self.velocity
        self.x2 -= self.velocity

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, window):
        window.blit(self.img, (self.x1, self.y))
        window.blit(self.img, (self.x2, self.y))

#Pipe Class
class Pipe:
    gap = 200
    velocity = 5

    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, 400)
        self.top = self.height - pipe_image.get_height()
        self.bottom = self.height + self.gap
        self.pipe_top = pygame.transform.flip(pipe_image, False, True)
        self.pipe_bottom = pipe_image
        self.passed = False

    def move(self):
        self.x -= self.velocity
    
    def draw(self, window):
        window.blit(self.pipe_top, (self.x, self.top))
        window.blit(self.pipe_bottom, (self.x, self.bottom))

    def off_screen(self):
        return self.x + pipe_image.get_width() < 0
    
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)

        offset_top = (self.x - bird.x, self.top - round(bird.y))
        offset_bottom = (self.x - bird.x, self.bottom - round(bird.y))

        if bird_mask.overlap(top_mask, offset_top) or bird_mask.overlap(bottom_mask, offset_bottom):
            return True
        
        return False
        
#Bird Class
class Bird:
    imgs = bird_images
    max_rotation = 25
    rot_velocity = 20
    animation_time = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.imgs[0]
    
    def jump(self):
        self.vel = -8  # This is the jump height so you can change it to make game hard or easy
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2 
        if d >= 16:
            d = 16
        
        if d < 0:
            d -= 2
        
        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.max_rotation:
                self.tilt = self.max_rotation
        else:
            if self.tilt > -90:
                self.tilt -= self.rot_velocity

    def draw(self, window):
        self.img_count += 1

        if self.img_count < self.animation_time:
            self.img = self.imgs[0]
        elif self.img_count < self.animation_time * 2:
            self.img = self.imgs[1]
        elif self.img_count < self.animation_time * 3:
            self.img = self.imgs[2]
        elif self.img_count < self.animation_time * 4:
            self.img = self.imgs[1]
        elif self.img_count == self.animation_time * 4 + 1:
            self.img = self.imgs[0]
            self.img_count = 0
        
        if self.tilt <= -80:
            self.img = self.imgs[1]
            self.img_count = self.animation_time

        # To make bird rotate in center of axis
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft=(self.x, self.y)).center)

        window.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


# Window of the game
def draw_window(window, bird, pipes, base, score):
    window.blit(background_image, (0, 0))

    for pipe in pipes:
        pipe.draw(window)
    
    text = stat_font.render(f"Score: {score}", 1, (255, 255, 255))
    window.blit(text, (width - 10 - text.get_width(), 10))
    base.draw(window)
    bird.draw(window)
    pygame.display.update()


# Game over
def game_over(window):
    game_over_x = (width - game_over_image.get_width()) // 2
    game_over_y = (height - game_over_image.get_height()) // 2

    window.blit(game_over_image, (game_over_x, game_over_y))
    pygame.display.update()
    pygame.time.delay(3000) # Delay after game over
    main() 

# Main
def main():
    pygame.display.set_caption("Flappy Bird with Code4FewBucks")
    
    bird = Bird(230,350)
    base= Base(730)
    pipes = [Pipe(700)]
    window = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    score = 0
    game_started = False

    while True:
        clock.tick(30)
        base.move()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_started = True
                bird.jump()
        
        if game_started:
            bird.move()

            for pipe in pipes:
                pipe.move()

                if pipe.collide(bird) or bird.y + bird_images[0].get_height() >= base.y:
                    game_over(window)
                
                if not pipe.passed and pipe.x + pipe_image.get_width() < bird.x:
                    pipe.passed = True
                    score += 1
                
                if pipe.off_screen():
                    pipes.remove(pipe)
            
            if pipes[-1].x < 400:
                pipes.append(Pipe(730))
        
        draw_window(window, bird, pipes, base, score)

if __name__ == "__main__":
    main()