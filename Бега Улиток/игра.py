


import pygame
import random
# Инициализация Pygame
pygame.init()
# Константы
WIDTH, HEIGHT = 800, 600
fon = pygame.image.load("fon-export.png")
background_image = pygame.image.load('fon_menu.png')
FPS = 60
SNAIL_COUNT = 3
FINISH_LINE_X = WIDTH - 50  # Позиция финишной линии
RACE_DURATION = 130  # Время гонки в секундах
# Инициализация Pygame
# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN= (0, 255, 0)
# Загрузка изображений улиток
snail_images = [
    pygame.image.load('улит_вп.png'),
    pygame.image.load('улит_гэрри.png'),
    pygame.image.load('улит_турбо.png')
]
# Загрузите изображение фона
#background_image = pygame.image.load('fon_menu.png')



class Snail:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = random.randint(1, 5)

    def move(self):
        self.rect.x += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def reset_game():
    """Сброс состояния игры."""
    return [Snail(snail_images[i], 100, 150 + i * 150) for i in range(SNAIL_COUNT)], [0] * SNAIL_COUNT, None, False
def main_menu():
    """Отображение главного меню."""

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Главное меню")
    clock = pygame.time.Clock()


    while True:
        screen.blit(background_image, (0, 0))
        font = pygame.font.Font(None, 35)
        title_text = font.render("Бегущие улитки", True, GREEN)
        start_text = font.render("Нажмите ENTER для начала", True, GREEN)
        exit_text = font.render("Нажмите ESC для выхода", True, GREEN)

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 50))


        pygame.display.flip()
        screen.blit(background_image, (0, 0))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Начать игру
                    main()
                if event.key == pygame.K_ESCAPE:  # Выйти из игры
                    pygame.quit()
                    return





def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Бегущие улитки")
    clock = pygame.time.Clock()

    snails, scores, winner, race_started = reset_game()
    start_ticks = pygame.time.get_ticks()
    timer = RACE_DURATION



    # Основной игровой цикл
    running = True
    while running:
        screen.blit(fon, (0, 0))
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # Сколько секунд прошло
        timer = RACE_DURATION - seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not race_started:
                    race_started = True  # Начинаем гонку
                if event.key == pygame.K_r:  # Перезапуск игры
                    snails, scores, winner, race_started = reset_game()
                    start_ticks = pygame.time.get_ticks()  # Сброс таймера
                    timer = RACE_DURATION

       # Рисуем фон



        # Отображаем улиток
        for snail in snails:
            snail.draw(screen)

        # Отображаем финишную линию
        pygame.draw.rect(screen, GREEN, (FINISH_LINE_X, 0, 5, HEIGHT))

        # Движение улиток
        if race_started and timer > 0 and winner is None:
            for i, snail in enumerate(snails):
                snail.move()
                if snail.rect.x > FINISH_LINE_X:
                    scores[i] += 1  # Увеличиваем очки за финиш
                    snail.rect.x = 50  # Сбросить позицию
                    snail.speed = random.randint(1, 5)  # Случайная скорость

            # Проверка на победителя
            max_score = max(scores)
            winners = [i for i, score in enumerate(scores) if score == max_score]

            if sum(scores) == 1:  # Один победитель
                winner = f"Улитка {winners[0] + 1} выиграла!"
            elif sum(scores)>1:  # Ничья
                winner = "Ничья!"

        # Отображаем таймер и очки
        font = pygame.font.Font(None, 36)

        score_text = font.render(f"Очки: {scores}", True, BLACK)

        screen.blit(score_text, (20, 50))

        # Если время вышло, выводим сообщение
        if timer <= 0:
            end_text = font.render("Время вышло!", True, BLACK)
            screen.blit(end_text, (WIDTH // 2 - 100, HEIGHT // 2))

        # Если есть победитель, выводим его имя
        if winner:
            winner_text = font.render(winner, True, BLACK)
            screen.blit(winner_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
            restart_text = font.render("Нажмите R для перезапуска", True, BLACK)
            screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 100))

            # Если гонка не началась, показываем инструкцию
        if not race_started:
            instruction_text = font.render("Нажмите SPACE для старта!", True, BLACK)
            screen.blit(instruction_text, (WIDTH // 2 - 150, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(FPS)



    pygame.quit()
if __name__ == "__main__":
 main_menu()
