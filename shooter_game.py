import pygame
import random

import game_sprite
import player
import enemy
import music


WIN_WIDTH = 700
WIN_HEIGHT = 500

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Shooter")
pygame.font.init()
font = pygame.font.Font(None, 36)

background = pygame.transform.scale(pygame.image.load("galaxy.jpg"), (WIN_WIDTH, WIN_HEIGHT))
ship = player.Player('rocket.png', 5, WIN_HEIGHT-100, 80, 100, 10, (WIN_WIDTH, WIN_HEIGHT))

enemys = []
for _ in range(6):
    enemys.append(enemy.Enemy("ufo.png", random.randint(80, WIN_WIDTH - 80), - 50, 80, 50, random.randint(1, 5), (WIN_WIDTH, WIN_HEIGHT)))

bullets = pygame.sprite.Group()

boss = enemy.Enemy("ufo.png", 0, -300, WIN_WIDTH, 400, 0, (WIN_HEIGHT, WIN_HEIGHT))

finish = False
game = True
lost = 0
score = 0
boss_fight = 10
asteroids = []

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.add(ship.fire())
                music.fire_sound.play()

    if not finish:
        window.blit(background, (0, 0))

        ship.update()
        bullets.update()

        window.blit(*ship.draw())

        if not asteroids:
            for _ in range(3):
                asteroids.append(enemy.Enemy('asteroid.png'), random.randint(80, WIN_WIDTH - 80), - 50, 80, 50, random.randint(1, 5), (WIN_WIDTH, WIN_HEIGHT))

        for asteroid in asteroids[:]:
            if asteroid.rect.colliderect(ship.rect):
                ship.hp -= 15
            if asteroid.update():
                asteroids.remove(asteroid)
            window.blit(*asteroid.draw())

        if score >= 2:
            window.blit(*boss.draw())
            
            for bullet in bullets:
                window.blit(*bullet.draw())
                if bullet.rect.colliderect(boss.rect):
                    boss_fight -= 1
                    bullet.kill()
            
            if boss_fight <= 0:
                window.blit(font.render(f'WIN!!!', 1, (255, 255, 255)), (WIN_WIDTH // 2 - 40, WIN_HEIGHT // 2))
                window.blit(font.render(f'Ты пропустил {lost} зефирок на землю', 1, (255, 255, 255)), (WIN_WIDTH // 2 - 140, WIN_HEIGHT // 2 + 30))

        else:
            
            for monster in enemys:
                window.blit(*monster.draw())
                if monster.update():
                    lost += 1

            for bullet in bullets:
                window.blit(*bullet.draw())
                for monster in enemys[:]:
                    if bullet.rect.colliderect(monster.rect):
                        enemys.remove(monster)
                        score += 1
                        bullet.kill()

            window.blit(font.render(f'Пропущено: {lost}', 1, (255, 255, 255)), (10, 20))
            window.blit(font.render(f'Счёт: {score}', 1, (255, 255, 255)), (10, 50))

            if lost >= 3:
                window.blit(font.render(f'Проиграл!!!', 1, (255, 255, 255)), (WIN_WIDTH // 2 - 40, WIN_HEIGHT // 2))
                window.blit(font.render(f'Ты пропустил {lost} зефирок на землю', 1, (255, 255, 255)), (WIN_WIDTH // 2 - 140, WIN_HEIGHT // 2 + 30))

            if len(enemys) < 6:
                enemys.append(enemy.Enemy("ufo.png", random.randint(80, WIN_WIDTH - 80), - 50, 80, 50, random.randint(1, 5), (WIN_WIDTH, WIN_HEIGHT)))


        pygame.display.update()
    pygame.time.delay(50)
