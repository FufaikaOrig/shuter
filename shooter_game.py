import pygame.time
from pygame import *
from Player import Player
from Enemy import Enemy, return_lost

import random
# создай окно игры
window = display.set_mode((700, 500))
display.set_caption("Shooter Game")


# задай фон сцены
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

spaceX = Player('rocket.png', 350, 400, 10, (65, 65), window)

copilots = [Enemy('ufo.png', random.randint(0, 700), 0,
                 random.randint(1, 4), (65, 65), window) for copilot in range(5)]
monsters = sprite.Group()
for copilot in copilots:
    monsters.add(copilot)


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound("fire.ogg")

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 36)

win = font.SysFont('Arial', 36)
lose = font.SysFont('Arial', 36)

bullets = sprite.Group()

score = 0
FPS = 30
clock = time.Clock()

# Переменные для контроля выстрелов
fire_rate = 250  # минимальный интервал между выстрелами в миллисекундах
last_shot = pygame.time.get_ticks()

game = True
finish = False
while game:

    # Установка ФПС
    clock.tick(FPS)
    text_lose = font1.render("Пропущено: " + str(return_lost()), 1, (255, 255, 255))
    text_kill = font2.render('Повержено:' + str(score), 1, (255, 255, 255))

    for e in event.get():
        # обработай событие «клик по кнопке "Закрыть окно"»
        if e.type == QUIT:
            game = False


    if not finish:
        window.blit(background, (0, 0))

        window.blit(text_lose, (0, 0))
        window.blit(text_kill, (0, 40))

        spaceX.update()

        keys = key.get_pressed()
        if keys[K_SPACE]:
            # Проверка интервала времени с последнего выстрела
            current_time = pygame.time.get_ticks()
            if current_time - last_shot >= fire_rate:
                spaceX.fire(bullets, fire)
                last_shot = current_time

        bullets.draw(window)
        bullets.update()

        spaceX.reset()

        monsters.draw(window)
        monsters.update()

        sprite_list = sprite.groupcollide(bullets, monsters, True, True)
        for bullet in sprite_list:
            score += len(sprite_list[bullet])
            monsters.add(Enemy('ufo.png', random.randint(0, 700), 0,
                 random.randint(1, 4), (65, 65), window))

        if score >= 10:
            finish = True
            win_game = font1.render("YOU WIN", 1, (255, 255, 255))
            window.blit(win_game, (250, 200))
        elif return_lost() >= 3 or sprite.spritecollide(spaceX, monsters, False):
            finish = True
            loose_game = font1.render("YOU LOOSE", 1, (255, 255, 255))
            window.blit(loose_game, (250, 200))

        display.update()
