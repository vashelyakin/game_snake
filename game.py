import random
import pygame

"""
Smooth snake game. Uses pygame library.

author: Vladislav Sheliakin
date: 2025.01.08
"""

pygame.init()

width = 1000
height = 1000

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

snake_list = []
x1, y1 = width / 2, height / 2

changeX1, changeY1 = 0, 0
snake_length = 1

snake_block = 20
snake_speed = 10  # Скорость в пикселях на тикa

foodX = random.randint(0, (width - snake_block) // snake_block) * snake_block
foodY = random.randint(0, (height - snake_block) // snake_block) * snake_block
pygame.mixer.music.load("assets/music_background.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
Sound_eat = pygame.mixer.Sound("assets/sound_eating.mp3")
bg = pygame.image.load("assets/sprite_background.png")
bg = pygame.transform.scale(bg, (width, height))
food_img = pygame.image.load("assets/sprite_food.png")

sprite_snake_head = pygame.image.load("assets/sprite_snake_head.png")
sprite_snake_head = pygame.transform.scale(sprite_snake_head, (snake_block, snake_block))

sprite_snake_tail = pygame.image.load("assets/sprite_snake_tail.png")
sprite_snake_tail = pygame.transform.scale(sprite_snake_tail, (snake_block, snake_block))

sprite_snake_body_straight = pygame.image.load("assets/sprite_snake_body_straight.png")
sprite_snake_body_straight = pygame.transform.scale(sprite_snake_body_straight, (snake_block, snake_block))

sprite_snake_body_turn = pygame.image.load("assets/sprite_snake_body_turn.png")
sprite_snake_body_turn = pygame.transform.scale(sprite_snake_body_turn, (snake_block, snake_block))

def eating(x1, y1, foodX, foodY):
    if foodX - snake_block <= x1 <= foodX + snake_block:
        if foodY - snake_block <= y1 <= foodY + snake_block:
            return True


def create_mes(msg, color, x, y,font_name, size):
    font_style = pygame.font.SysFont(font_name, size)
    mes = font_style.render(msg, True, color)
    screen.blit(mes, [x, y])


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Smooth Snake")

random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

FPS = 30
clock = pygame.time.Clock()
def game_lose():
    snake_list = []
    x1, y1 = width / 2, height / 2

    changeX1, changeY1 = 0, 0
    snake_length = 1

    snake_block = 20
    snake_speed = 10  # Скорость в пикселях на тикa

    foodX = random.randint(0, (width - snake_block) // snake_block) * snake_block
    foodY = random.randint(0, (height - snake_block) // snake_block) * snake_block
    game_close = False
    run = True
    while run:
        clock.tick(FPS)
        while game_close:
            screen.fill("red")
            create_mes("You lose!!!!!!!!!!!!", black, 450, 500, "calibri",50)
            create_mes('Нажмите на "Q" чтобы выйти из игры!', black, 200, 600, "calibri", 50)
            create_mes('Нажмите на "C" чтобы перезапустить игру!', black, 100, 700, "Verdana", 40)
            create_mes(f"Your Score: {snake_length - 1}", "yellow", 450, 550, "Verdana", 40)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        game_lose()


        for event in pygame.event.get():
            # exit the game
            if event.type == pygame.QUIT:
                run = False
            # control snake turns. We can turn only 90 degree
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and changeX1 == 0:
                    changeX1 = -snake_speed
                    changeY1 = 0
                elif event.key == pygame.K_d and changeX1 == 0:
                    changeX1 = snake_speed
                    changeY1 = 0
                elif event.key == pygame.K_w and changeY1 == 0:
                    changeX1 = 0
                    changeY1 = -snake_speed
                elif event.key == pygame.K_s and changeY1 == 0:
                    changeX1 = 0
                    changeY1 = snake_speed

        x1 += changeX1
        y1 += changeY1

        # draw the background
        screen.blit(bg, (0, 0))
        create_mes(f"Score: {snake_length - 1}", "red",  20, 20, "segoeuihistoric", 50)

        # draw food rectangle
        #pygame.draw.rect(screen, red, [foodX, foodY, snake_block, snake_block])

        # draw image food
        screen.blit(food_img, (foodX, foodY))

        # hitbox check
        if eating(x1, y1, foodX, foodY):
            foodX = random.randint(0, (width - snake_block) // snake_block) * snake_block
            foodY = random.randint(0, (height - snake_block) // snake_block) * snake_block
            snake_length += 1
            Sound_eat.play()

        # get coordinates of snake's head
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # draw the snake body from tail to head
        counter = 0
        for i in snake_list:
            if counter == (snake_length - 1):
                # draw the head
                snake_head_angle = 0
                if changeX1 < 0 and changeY1 == 0:
                    snake_head_angle = 270
                if changeX1 > 0 and changeY1 == 0:
                    snake_head_angle = 90
                if changeX1 == 0 and changeY1 < 0:
                    snake_head_angle = 180
                if changeX1 == 0 and changeY1 > 0:
                    snake_head_angle = 0
                screen.blit(pygame.transform.rotate(sprite_snake_head, snake_head_angle), (i[0], i[1]))
            elif counter == 0 and snake_length > 1:
                # draw the tail
                snake_tail_angle = 0
                if snake_list[counter][0] < snake_list[counter + 1][0] and snake_list[counter][1] == snake_list[counter + 1][1]:
                    snake_tail_angle = 90
                if snake_list[counter][0] > snake_list[counter + 1][0] and snake_list[counter][1] == snake_list[counter + 1][1]:
                    snake_tail_angle = 270
                if snake_list[counter][0] == snake_list[counter + 1][0] and snake_list[counter][1] < snake_list[counter + 1][1]:
                    snake_tail_angle = 180
                if snake_list[counter][0] == snake_list[counter + 1][0] and snake_list[counter][1] > snake_list[counter + 1][1]:
                    snake_tail_angle = 0
                screen.blit(pygame.transform.rotate(sprite_snake_tail, snake_tail_angle), (i[0], i[1]))
            elif snake_length > 2:
                #pygame.draw.rect(screen, green, [i[0], i[1], snake_block, snake_block])
                # draw remain body
                # first straight pieces
                # all vertical
                if snake_list[counter - 1][0] == snake_list[counter + 1][0]:
                    screen.blit(pygame.transform.rotate(sprite_snake_body_straight, 0), (i[0], i[1]))
                # horizontal
                if snake_list[counter - 1][1] == snake_list[counter + 1][1]:
                    screen.blit(pygame.transform.rotate(sprite_snake_body_straight, 90), (i[0], i[1]))

                # bend the snake
                snake_element_maxx = max(snake_list[counter - 1][0], snake_list[counter + 1][0])
                snake_element_maxy = max(snake_list[counter - 1][1], snake_list[counter + 1][1])

                # when go down
                # left bottom angle
                if snake_list[counter][0] < snake_element_maxx and snake_list[counter][1] == snake_element_maxy:
                    screen.blit(pygame.transform.rotate(sprite_snake_body_turn, 0), (i[0], i[1]))
                # right upper angle
                if snake_list[counter][0] == snake_element_maxx and snake_list[counter][1] < snake_element_maxy:
                    screen.blit(pygame.transform.rotate(sprite_snake_body_turn, 180), (i[0], i[1]))
                # left upper angle
                if snake_list[counter][0] < snake_element_maxx and snake_list[counter][1] < snake_element_maxy:
                    screen.blit(pygame.transform.rotate(sprite_snake_body_turn, 270), (i[0], i[1]))
                # right bottom angle
                if snake_list[counter][0] == snake_element_maxx and snake_list[counter][1] == snake_element_maxy:
                    screen.blit(pygame.transform.rotate(sprite_snake_body_turn, 90), (i[0], i[1]))

            counter = counter + 1

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        pygame.display.flip()

    pygame.quit()
game_lose()
