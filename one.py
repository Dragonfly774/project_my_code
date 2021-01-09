import os
import sys

import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Hero(pygame.sprite.Sprite):
    def __init__(self, grop):
        super().__init__(grop)
        self.images = []
        self.images.append(load_image('creature4.png'))
        self.images.append(load_image('raight1.png'))
        self.images.append(load_image('left1.png'))
        self.right = True
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0

    def update_index(self, index):

        self.index = index
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def update(self):
        self.rect.x += self.change_x

    # Передвижение игрока
    def go_left(self):
        self.change_x = -9  # Двигаем игрока по Х
        if self.right:  # Проверяем куда он смотрит, то переворачиваем его
            self.update_index(2)
            self.right = False

    def go_right(self):
        # то же самое, но вправо
        self.change_x = 9
        if not self.right:
            self.update_index(1)
            self.right = True

    def stop(self):
        # вызываем этот метод, когда не нажимаем на клавиши
        self.change_x = 0


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def main():
    pygame.init()
    pygame.display.set_caption('Никита сказал')
    size = width, height = 640, 500
    screen = pygame.display.set_mode(size)

    running = True
    pygame.mouse.set_visible(False)
    all_sprites = pygame.sprite.Group()
    hero = Hero(all_sprites)
    clock = pygame.time.Clock()

    hero.rect.x = 340
    hero.rect.y = 350  # height - hero.rect.height

    background = Background('data/background4.jpg', [0, 0])
    while running:
        screen.fill([255, 255, 255])
        screen.blit(background.image, background.rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    hero.update_index(2)
                    hero.go_left()

                if event.key == pygame.K_RIGHT:
                    hero.update_index(1)
                    hero.go_right()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and hero.change_x < 0:
                    hero.stop()
                    hero.update_index(0)

                if event.key == pygame.K_RIGHT and hero.change_x > 0:
                    hero.stop()
                    hero.update_index(0)

        all_sprites.update()

        # Если игрок приблизится к правой стороне, то дальше его не двигаем
        if hero.rect.right > width:
            hero.rect.right = width

        # Если игрок приблизится к левой стороне, то дальше его не двигаем
        if hero.rect.left < 0:
            hero.rect.left = 0

        clock.tick(30)
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
